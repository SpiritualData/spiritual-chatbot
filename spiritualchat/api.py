"""
Uses query_chatbot to send chatbot response back to user.

Request:
{
    "conversation_id": "123456",
    "chat_history": [
        {
            "user": "Tell me more about near death experiences.",
            "ai": "Near-death experiences are profound psychological events..."
        }
    ],
    "user_input": "What experiences talk about users?"
}
Response:
{
    "ai_response": "Spiritual science attempts to investigate spiritual experiences, including phenomena like metaphysics and near-death experiences, through rigorous and scholarly methodologies. While it may not provide definitive answers, it offers valuable insights and frameworks for understanding these complex phenomena.",

    "db_results": {
        "hypotheses": [
            {
                "url": "https://www.example.com/hypothesis1",
                "name": "Exploring Metaphysical Realities: Hypotheses in Contemporary Philosophy",
                "snippet": "Our hypothesis posits that metaphysics, when interpreted through the lens of spiritual science, can be understood as a pursuit of the ultimate nature of spiritual and physical reality."
            }
        ],
        "experiences": [
            {
                "url": "https://www.example.com/experience1",
                "name": "Tales of the Beyond: An Anthology of Near-Death Experiences",
                "snippet": "In our collection of near-death experiences, many narrators reported a profound sense of interconnectedness and spiritual awakening, suggesting possible ties with metaphysical principles."
            }
        ],
        "research": [
            {
                "url": "https://www.example.com/research1",
                "name": "Spiritual Science: An Empirical Analysis of Metaphysical and Near-Death Phenomena",
                "snippet": "Our research aimed to apply the tools of spiritual science to better understand metaphysics and near-death experiences. While conclusions remain tentative, our findings underscore the potential value of spiritual perspectives in these areas."
            }
        ]
    }
}
"""

from spiritualchat import query_chatbot

