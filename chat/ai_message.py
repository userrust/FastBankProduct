from openai import AsyncOpenAI
import re

AI_TOKEN = "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"
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_TOKEN,
)


async def ai_generate(text: str):
    completion = await client.chat.completions.create(

        model="deepseek/deepseek-chat",
        messages=[
            {
                "role":"user",
                "content":"Ты используешься как тех подержка для банкавского приложения FastBank тебе"
                "будет задан вопрос по поводу банковсого приложения операцие итд ответь на него точно и понятно"
                "если вопро не по теме скажи об это и предложи ответеь на вопрос по теме но если это преветствие"
                " или выражения дружелюьия ответь на это. А вот и сам вопрос :" + text
            }
        ]
    )
    print(completion)

    ai_text = completion.choices[0].message.content
    cleaned_text = re.sub(r'[\\\[\]{}()*]', '', ai_text)
    # Удаляем лишние пробелы и пустые строки

    cleaned_text1 = re.sub(r'\n\s*\n', '\n', cleaned_text)  # Удаляем пустые строки
    cleaned_text2 = cleaned_text1.strip()  # Убираем пробелы в начале и конце
    return cleaned_text2

