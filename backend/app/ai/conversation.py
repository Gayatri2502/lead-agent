"""AI conversation and intent handling"""
import json
import logging
from typing import Optional, Dict, List
from datetime import datetime
from app.schemas import AppointmentCreate

logger = logging.getLogger(__name__)


class ConversationContext:
    """Maintain conversation state"""
    
    def __init__(self, customer_id: Optional[int] = None, business_id: int = None):
        self.customer_id = customer_id
        self.business_id = business_id
        self.messages: List[Dict[str, str]] = []
        self.detected_intent: Optional[str] = None
        self.extracted_data: Dict = {}
        self.conversation_state = "greeting"  # greeting, collecting_info, confirming, closing
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_messages_for_api(self) -> List[Dict[str, str]]:
        """Get messages in OpenAI format"""
        return [{"role": m["role"], "content": m["content"]} for m in self.messages]


class IntentDetector:
    """Detect customer intent from conversation"""
    
    INTENTS = {
        "book": ["book", "appointment", "schedule", "reserve", "make appointment"],
        "reschedule": ["reschedule", "change", "move", "different time", "can't make it"],
        "cancel": ["cancel", "cancel appointment", "no longer need"],
        "inquire": ["what", "how much", "tell me about", "information", "services"],
        "availability": ["available", "when can", "next appointment", "free slot"],
        "emergency": ["emergency", "urgent", "help", "pain", "severe"],
        "speak_human": ["speak to someone", "human", "representative", "operator"]
    }
    
    @staticmethod
    def detect(text: str) -> str:
        """Detect intent from text"""
        text_lower = text.lower()
        
        for intent, keywords in IntentDetector.INTENTS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        return "inquire"


class AppointmentAgent:
    """Handle appointment booking logic"""
    
    def __init__(self, db=None):
        self.db = db
    
    def extract_customer_info(self, context: ConversationContext) -> dict:
        """Extract customer information from conversation"""
        info = {}
        
        # Simple pattern matching (in production, use NLP)
        for message in context.messages:
            if message["role"] == "user":
                text = message["content"].lower()
                
                # Extract phone (basic pattern)
                if any(char.isdigit() for char in text) and len([c for c in text if c.isdigit()]) >= 7:
                    info["phone"] = ''.join(filter(str.isdigit, text))
                
                # Extract email
                if "@" in text:
                    words = text.split()
                    for word in words:
                        if "@" in word and "." in word:
                            info["email"] = word
        
        return info
    
    def build_appointment_data(self, context: ConversationContext) -> Optional[AppointmentCreate]:
        """Build appointment creation data from extracted info"""
        data = context.extracted_data
        
        if not all(k in data for k in ["customer_id", "start_time", "service_id"]):
            return None
        
        return AppointmentCreate(
            customer_id=data["customer_id"],
            staff_id=data.get("staff_id"),
            service_id=data.get("service_id"),
            start_time=data["start_time"],
            duration=data.get("duration", 30),
            reason=data.get("reason"),
            notes=data.get("notes"),
            booking_source="phone"
        )


class CallSummarizer:
    """Generate call summaries"""
    
    @staticmethod
    def generate_summary(transcript: str, intent: str) -> str:
        """Generate concise summary of call"""
        if not transcript:
            return ""
        
        # Simple summarization (in production, use GPT)
        lines = transcript.split("\n")
        key_points = [line for line in lines if any(keyword in line.lower() 
                     for keyword in ["appointment", "booked", "cancelled", "error", "problem"])]
        
        summary = f"Intent: {intent}. "
        if key_points:
            summary += "Key points: " + "; ".join(key_points[:3])
        else:
            summary += "Standard inquiry."
        
        return summary


class SentimentAnalyzer:
    """Analyze call sentiment"""
    
    @staticmethod
    def analyze(transcript: str) -> str:
        """Analyze sentiment from transcript"""
        if not transcript:
            return "neutral"
        
        # Simple sentiment analysis (in production, use ML model)
        positive_words = ["great", "perfect", "thank", "appreciate", "happy", "excellent", "good"]
        negative_words = ["angry", "frustrated", "problem", "issue", "terrible", "bad", "worst"]
        
        text_lower = transcript.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
