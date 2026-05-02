"""
Emotional Analysis and Crisis Detection Service

Analyzes user messages to detect emotional patterns and identify crisis indicators.
Stores insights for personalized chatbot responses.
"""

from datetime import datetime, timedelta
from models import db, EmotionalInsight, ChatMessage, User


# Crisis/Safety keywords that require immediate intervention
CRISIS_KEYWORDS = {
    'self_harm': [
        'tự tử', 'tử vong', 'chết', 'không sống được', 'không đáng sống',
        'tự làm hại bản thân', 'cắt tay', 'uống thuốc độc', 'nhảy từ tầng cao',
        'hang cổ', 'không muốn sống', 'muốn kết thúc', 'không có ý nghĩa'
    ],
    'hopelessness': [
        'vô vọng', 'tuyệt vọng', 'không có hy vọng', 'không có cách nào',
        'tất cả đều vô ích', 'không bao giờ tốt lên', 'bẩm sinh lỗi',
        'không đáng ngồi', 'mọi thứ đều tồi tệ', 'không thể khác'
    ],
    'severe_abuse': [
        'bị lạm dụng', 'bị hành hạ', 'bạo lực', 'đòn roi', 'khủng bố',
        'bị lạm dụng tình dục'
    ]
}

# Emotional signal keywords for pattern recognition
EMOTIONAL_SIGNALS = {
    'stress': [
        'căng thẳng', 'stress', 'áp lực', 'không chịu nổi', 'quá tải',
        'áp lực lớn', 'không kịp', 'deadline', 'bận rộn vô cùng'
    ],
    'anxiety': [
        'lo lắng', 'cảm giác sợ hãi', 'hoảng sợ', 'nơm nớp', 'sợ',
        'lo sợ', 'bồn chồn', 'đảo lộn', 'không yên'
    ],
    'sadness': [
        'buồn', 'chán nản', 'buồn rũ', 'cô đơn', 'khó chịu', 'tổn thương',
        'tuyệt vọng (nhẹ)', 'chán đời', 'côi cút', 'mất mát'
    ],
    'burnout': [
        'kiệt sức', 'mệt mỏi', 'mệt lả', 'đã chán', 'không còn động lực',
        'hư hỏng', 'kiệt quệ', 'không chịu nỗi', 'cảm giác bế tắc'
    ],
    'overwhelm': [
        'choáng ngợp', 'quá sức', 'không xử lý nổi', 'không biết phải làm gì',
        'bộ não hỏng', 'tư duy lộn xộn', 'rối loạn'
    ]
}

JOURNAL_PROMPTS = [
    'Hôm nay bạn muốn ghi lại điều gì? Hãy bắt đầu bằng một câu đơn giản.',
    'Viết về một khoảnh khắc vừa qua khiến bạn cảm thấy nhẹ nhõm hoặc khó chịu.',
    'Mô tả một điều bạn biết ơn hôm nay, dù nhỏ bé đến đâu.',
    'Bạn đã gặp phải thử thách nào hôm nay? Bạn đã phản ứng thế nào?',
    'Hãy kể về cảm xúc hiện tại của bạn và điều bạn muốn lắng nghe từ chính mình.',
    'Viết một câu hỏi bạn muốn tự hỏi mình trong một ngày khó khăn.',
]

EMOTION_PROMPTS = {
    '🙂': 'Bạn đang vui. Hãy viết về điều giúp bạn cảm thấy tốt và cách duy trì tâm trạng này.',
    '😢': 'Bạn đang buồn. Hãy viết về nguyên nhân và điều bạn có thể làm để nhẹ lòng hơn.',
    '😡': 'Bạn đang giận. Hãy mô tả điều khiến bạn khó chịu và cách bạn muốn đối xử với mình bây giờ.',
    '😨': 'Bạn đang lo lắng. Hãy viết về điều làm bạn sợ và những điều nhỏ bạn có thể làm để an tâm hơn.',
    '😴': 'Bạn đang mệt mỏi. Hãy viết về điều làm bạn cạn năng lượng và điều bạn cần nghỉ ngơi.',
    '❤️': 'Bạn đang biết ơn. Hãy viết về điều người hoặc sự việc khiến bạn cảm thấy ấm lòng.',
}

REFLECTION_PROMPTS = [
    'Sau khi viết xong, bạn có thể hỏi: "Điều này giúp mình hiểu gì về bản thân?"',
    'Bạn có thể ghi thêm: "Mình học được gì từ trải nghiệm này?"',
    'Hãy suy ngẫm: "Mình cần thứ gì nhất lúc này để cảm thấy ổn hơn?"',
    'Viết một câu: "Nếu mình nói với người bạn thân, mình sẽ nói gì?"',
]

JOURNAL_TEMPLATES = {
    'what_happened': {
        'label': 'Chuyện gì đã xảy ra / Cảm xúc của tôi',
        'text': 'Chuyện gì đã xảy ra?\nCảm xúc của tôi là gì?\nMình muốn điều gì tiếp theo?'
    },
    'what_i_felt': {
        'label': 'Điều tôi cảm nhận / Điều tôi cần',
        'text': 'Điều tôi cảm nhận:\nĐiều tôi cần bây giờ: '
    },
    'gratitude': {
        'label': 'Biết ơn / Lấy cảm hứng',
        'text': 'Mình biết ơn điều gì hôm nay?\nLàm điều đó khiến mình thấy thế nào?'
    }
}


def get_journal_prompt(emotion=None):
    """Return a guided journal prompt, adapting to emotion when available."""
    if emotion and emotion in EMOTION_PROMPTS:
        return EMOTION_PROMPTS[emotion]
    if not JOURNAL_PROMPTS:
        return ''
    index = datetime.utcnow().day % len(JOURNAL_PROMPTS)
    return JOURNAL_PROMPTS[index]


def get_reflection_prompt():
    """Return a follow-up reflection prompt."""
    if not REFLECTION_PROMPTS:
        return ''
    index = datetime.utcnow().day % len(REFLECTION_PROMPTS)
    return REFLECTION_PROMPTS[index]


def get_journal_templates():
    """Return structured journal template options."""
    return list(JOURNAL_TEMPLATES.values())


def detect_crisis_signals(user_message: str) -> tuple[bool, str]:
    """
    Detect if user message contains crisis/safety indicators.
    
    Returns (is_crisis, crisis_type)
    """
    message_lower = user_message.lower()
    
    for crisis_type, keywords in CRISIS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                return True, crisis_type
    
    return False, ""


def detect_emotional_signals(user_message: str) -> list[tuple[str, float]]:
    """
    Detect emotional signals in user message.
    Returns list of (emotion_type, confidence) tuples.
    """
    signals = []
    message_lower = user_message.lower()
    word_count = len(message_lower.split())
    
    for emotion_type, keywords in EMOTIONAL_SIGNALS.items():
        matches = sum(1 for keyword in keywords if keyword in message_lower)
        if matches > 0:
            # Confidence based on keyword density
            confidence = min(1.0, (matches / len(keywords)) * (matches / max(1, word_count / 5)))
            signals.append((emotion_type, confidence))
    
    return sorted(signals, key=lambda x: x[1], reverse=True)


def store_emotional_insight(user_id: int, emotion_type: str, message_content: str, trigger: str = None):
    """
    Store an emotional insight from user message.
    
    If similar insight exists recently, update frequency instead of creating new.
    """
    # Check if similar insight exists within last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    existing = EmotionalInsight.query.filter_by(
        user_id=user_id,
        emotion_type=emotion_type
    ).filter(
        EmotionalInsight.created_at >= seven_days_ago
    ).first()
    
    if existing:
        # Update existing insight
        existing.last_observed = datetime.utcnow()
        
        # Increase frequency
        freq_map = {'rare': 'occasional', 'occasional': 'frequent', 'frequent': 'frequent'}
        existing.frequency = freq_map.get(existing.frequency, 'occasional')
        
        db.session.commit()
        return existing
    else:
        # Create new insight
        # Extract key phrase from message (first 100 chars or first sentence)
        description = message_content[:150]
        if len(message_content) > 150:
            description = description.rsplit(' ', 1)[0] + '...'
        
        insight = EmotionalInsight(
            user_id=user_id,
            emotion_type=emotion_type,
            description=description,
            trigger=trigger,
            frequency='occasional'
        )
        db.session.add(insight)
        db.session.commit()
        return insight


def get_user_emotional_context(user_id: int, limit: int = 5) -> str:
    """
    Retrieve recent emotional insights for a user to inject into chatbot prompt.
    
    Returns formatted string of insights or empty string if none exist.
    """
    insights = EmotionalInsight.query.filter_by(
        user_id=user_id
    ).order_by(
        EmotionalInsight.last_observed.desc()
    ).limit(limit).all()
    
    if not insights:
        return ""
    
    context = "\n[User's Emotional Patterns]\n"
    for insight in insights:
        trigger_str = f" (when {insight.trigger})" if insight.trigger else ""
        context += f"• {insight.emotion_type.capitalize()}: {insight.description}{trigger_str}\n"
    
    context += "\n"
    return context


def get_crisis_response() -> str:
    """
    Return safe, supportive response for crisis detection.
    """
    return """Tôi nhận thấy bạn đang trải qua những cảm xúc rất khó khăn. Mình rất quan tâm tới bạn.

🆘 **Bạn không cần phải chịu đựng một mình. Vui lòng liên hệ với những người có thể giúp đỡ:**

🇻🇳 **Tại Việt Nam:**
• **Đường dây nóng Tư vấn tâm lý**: 1900.969.885 (miễn phí, 24/7)
• **Trung tâm Hỗ trợ Cô đơn & Tuyệt vọng**: 024.62.686.686
• **Bệnh viện Tâm thần Việt Đức**: 024.37.566.888
• **Bệnh viện Tâm thần Trung ương**: 024.35.556.555
• **Nhóm hỗ trợ tâm lý trực tuyến VietMind**: https://vietmind.org

💬 **Hãy kể cho ai đó bạn tin tưởng biết về cảm giác của bạn:**
- Cha mẹ, anh chị em
- Bạn bè thân thiết
- Giáo viên hoặc cố vấn học tập
- Bác sĩ hoặc nhân viên y tế

**Mình ở đây để hỗ trợ, nhưng những người bên ngoài với đào tạo chuyên môn có thể giúp bạn tốt hơn. Bạn xứng đáng được chăm sóc chuyên nghiệp. ❤️**"""


def generate_personalized_prompt_injection(user_id: int) -> str:
    """
    Generate prompt injection with user's emotional context for chatbot.
    """
    context = get_user_emotional_context(user_id)
    
    if context:
        return f"""{context}[When responding, gently reference these patterns if relevant. For example:
"Tôi nhớ bạn từng nói về {context.split('•')[1][:30]}... Cảm xúc đó có quay trở lại không?"]

"""
    
    return ""


def analyze_and_store_insights(user_id: int, message_content: str) -> None:
    """
    Main function: Analyze message and store any detected emotional insights.
    """
    # Detect emotional signals
    signals = detect_emotional_signals(message_content)
    
    # Store top signal as insight
    if signals:
        top_emotion, confidence = signals[0]
        if confidence > 0.3:  # Only store if confidence is reasonable
            store_emotional_insight(
                user_id=user_id,
                emotion_type=top_emotion,
                message_content=message_content,
                trigger="conversation with chatbot"
            )
