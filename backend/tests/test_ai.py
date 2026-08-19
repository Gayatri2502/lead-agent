"""AI agent integration tests"""
import pytest
from app.ai.conversation import (
    ConversationContext,
    IntentDetector,
    AppointmentAgent,
    CallSummarizer,
    SentimentAnalyzer,
)


class TestIntentDetection:
    def test_detect_booking_intent(self):
        text = "I'd like to book an appointment"
        intent = IntentDetector.detect(text)
        assert intent == "book"

    def test_detect_cancel_intent(self):
        text = "I need to cancel my appointment"
        intent = IntentDetector.detect(text)
        assert intent == "cancel"

    def test_detect_reschedule_intent(self):
        text = "Can I move my appointment to a different time?"
        intent = IntentDetector.detect(text)
        assert intent == "reschedule"


class TestConversationContext:
    def test_add_message(self):
        context = ConversationContext(customer_id=1, business_id=1)
        context.add_message("user", "Hello")
        context.add_message("assistant", "Hi there!")

        assert len(context.messages) == 2
        assert context.messages[0]["role"] == "user"
        assert context.messages[0]["content"] == "Hello"

    def test_get_messages_for_api(self):
        context = ConversationContext()
        context.add_message("user", "Test message")
        
        messages = context.get_messages_for_api()
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "Test message"


class TestCallSummarizer:
    def test_generate_summary(self):
        transcript = "Customer called to book an appointment for Monday at 2 PM"
        summary = CallSummarizer.generate_summary(transcript, "book")
        
        assert summary is not None
        assert "book" in summary.lower()

    def test_generate_summary_empty(self):
        summary = CallSummarizer.generate_summary("", "inquire")
        assert summary == ""


class TestSentimentAnalyzer:
    def test_positive_sentiment(self):
        transcript = "Thank you so much! This is great and I appreciate your help!"
        sentiment = SentimentAnalyzer.analyze(transcript)
        assert sentiment == "positive"

    def test_negative_sentiment(self):
        transcript = "This is terrible, I'm very frustrated and angry about this problem"
        sentiment = SentimentAnalyzer.analyze(transcript)
        assert sentiment == "negative"

    def test_neutral_sentiment(self):
        transcript = "I need to schedule an appointment"
        sentiment = SentimentAnalyzer.analyze(transcript)
        assert sentiment == "neutral"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
