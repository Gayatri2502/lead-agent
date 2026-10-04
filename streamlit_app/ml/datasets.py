"""Training data generation for the receptionist intent classifier.

The dataset is *derived from the user's agent configuration*: role vocabulary,
services, and business name all shape the caller utterances. This is what makes
the trained model behave like a receptionist for the designated role.
"""
from __future__ import annotations

import hashlib
import random
from typing import Any, Dict, List, Tuple

INTENTS = [
    "greeting", "goodbye", "book_appointment", "reschedule_appointment",
    "cancel_appointment", "check_availability", "ask_services", "ask_price",
    "ask_hours", "ask_location", "ask_human", "affirm", "deny", "fallback_filler",
]

_GENERICS = {
    "greeting": [
        "hi", "hello", "hey there", "good morning", "good afternoon", "good evening",
        "hi, is this {business}", "hello, {business}?", "hi, who am i speaking with",
        "hello, i need some help", "hey, are you open today", "hi there, how are you",
        "good morning, i have a question", "hello hello", "hi, can you hear me",
    ],
    "goodbye": [
        "bye", "goodbye", "that's all, thanks", "thank you, bye", "see you later",
        "thanks for your help, bye", "ok bye now", "have a great day", "that's everything, thank you",
        "no that's all, bye", "appreciate it, goodbye", "talk soon, bye",
    ],
    "book_appointment": [
        "i'd like to book an appointment", "i want to schedule a {service}",
        "can i book a {service}", "i need to make an appointment", "book me in for a {service}",
        "i want to come in for a {service}", "can i get an appointment for a {service}",
        "i'd like to schedule something", "do you have any openings for a {service}",
        "set up an appointment please", "i need a {service} this week",
        "can i arrange a {service}", "i'm calling to book", "i would like to make a booking",
        "can we set up a visit", "put me down for a {service}",
        "i'm looking to book a {service} appointment", "schedule me for a {service} please",
        "hi, i want to book", "i need to see someone for a {service}",
    ],
    "reschedule_appointment": [
        "i need to reschedule my appointment", "can i move my {service} to another day",
        "something came up, can we change my appointment", "i want to change my booking",
        "can we push my appointment to next week", "i need to move my {service}",
        "is it possible to reschedule", "change my appointment time please",
        "i can't make it at that time anymore", "shift my appointment to friday",
        "reschedule my visit please", "i'd like to pick a different time",
    ],
    "cancel_appointment": [
        "i need to cancel my appointment", "cancel my {service} please",
        "i can't make it, please cancel", "i want to cancel my booking",
        "please cancel my visit", "i have to cancel", "remove my appointment",
        "cancel the {service} i booked", "i won't be able to come in",
        "call off my appointment", "i'd like to cancel", "scratch my appointment",
    ],
    "check_availability": [
        "what times do you have available", "are there any openings this week",
        "what's your availability like", "do you have anything open tomorrow",
        "when is your next available slot", "any free slots on friday",
        "check availability for me", "what appointments are open",
        "is there space on saturday", "what do you have available next week",
        "when can i come in", "show me open times", "any availability today",
    ],
    "ask_services": [
        "what services do you offer", "what can i book there", "tell me about your services",
        "what do you do at {business}", "what treatments are available",
        "what kind of services do you have", "what are my options",
        "do you offer {service}", "can you tell me what you provide",
        "what's on your menu of services", "what do you offer", "list your services please",
    ],
    "ask_price": [
        "how much does a {service} cost", "what's the price of a {service}",
        "how much is a {service}", "what do you charge for a {service}",
        "can you tell me your prices", "how much will it cost",
        "what's the cost of a visit", "pricing information please",
        "is a {service} expensive", "what are your rates",
        "how much do you charge", "price for {service} please",
    ],
    "ask_hours": [
        "what are your hours", "when are you open", "what time do you close",
        "are you open on weekends", "what time do you open",
        "are you open right now", "business hours please",
        "how late are you open", "when do you close today",
        "are you open on sunday", "tell me your opening hours", "when can i visit",
    ],
    "ask_location": [
        "where are you located", "what's your address", "how do i get there",
        "where is your office", "can you give me directions",
        "where do i find you", "what's the location",
        "are you downtown", "what street are you on", "where should i come",
    ],
    "ask_human": [
        "can i speak to a person", "i want to talk to a human", "transfer me to a manager",
        "is there a real person i can talk to", "connect me with a staff member",
        "i need to speak with someone", "get me a human please",
        "transfer me to the front desk", "let me talk to an actual person",
        "can someone call me back", "i'd rather speak to a person",
    ],
    "affirm": [
        "yes", "yes please", "yeah", "yep", "sure", "sounds good", "correct",
        "that's right", "absolutely", "definitely", "ok", "okay", "perfect",
        "that works", "yes that's fine", "confirmed", "go ahead", "please do",
    ],
    "deny": [
        "no", "nope", "no thanks", "not really", "that's not right",
        "no, that's wrong", "i don't think so", "negative", "no thank you",
        "not that one", "no way", "that's not what i meant", "nah", "never mind",
    ],
    "fallback_filler": [
        "um", "uhh", "hmm let me think", "hold on a sec", "wait what was i saying",
        "sorry one moment", "let me check my calendar quickly", "ummm", "err",
        "can you hold on", "just a second", "hm", "ah right", "well", "so yeah",
    ],
}

# Role-flavored extra samples: vocabulary words injected into booking/pricing asks
_ROLE_BOOST_TEMPLATES = [
    ("book_appointment", "i need someone to look at my {vocab}"),
    ("book_appointment", "can i get an appointment, it's about my {vocab}"),
    ("ask_services", "do you handle {vocab}"),
    ("ask_price", "what do you charge for {vocab} work"),
    ("check_availability", "when can someone see me about my {vocab}"),
]


def _config_seed(cfg: Dict[str, Any]) -> int:
    basis = "|".join([
        cfg.get("role", ""), cfg.get("business_name", ""),
        ",".join(s.get("name", "") for s in cfg.get("services", [])),
    ])
    return int(hashlib.sha256(basis.encode()).hexdigest()[:8], 16)


def build_dataset(cfg: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Return (utterance, intent) pairs tailored to the agent configuration."""
    rng = random.Random(_config_seed(cfg))
    services = [s["name"] for s in cfg.get("services", [])] or ["appointment"]
    business = cfg.get("business_name", "the office")
    vocab = cfg.get("vocabulary") or []

    samples: List[Tuple[str, str]] = []

    def render(template: str) -> str:
        return template.replace("{service}", rng.choice(services)).replace("{business}", business)

    for intent, templates in _GENERICS.items():
        renders = {render(t) for t in templates}
        # light augmentation: punctuation/casing variants keep it robust
        augmented = set()
        for text in renders:
            augmented.add(text)
            augmented.add(text + rng.choice(["", "?", ".", " please"]))
            augmented.add(text.capitalize())
        samples.extend((t, intent) for t in augmented)

    # Role vocabulary boosts
    for word in vocab:
        for intent, template in _ROLE_BOOST_TEMPLATES:
            samples.append((template.replace("{vocab}", word), intent))

    # FAQ-style questions teach the model real Q&A phrasing for this business
    for faq in cfg.get("faqs", []):
        q = (faq.get("q") or "").strip().lower().rstrip("?")
        if q:
            samples.append((q, "ask_services"))

    rng.shuffle(samples)
    return samples


def dataset_stats(samples: List[Tuple[str, str]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for _, intent in samples:
        counts[intent] = counts.get(intent, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True))
