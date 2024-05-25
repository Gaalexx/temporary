"""
model - Выбор модели для генерации ("GigaChat", "GigaChat-preview", "GigaChat-Plus", "GigaChat-Pro", "GigaChat-Pro-preview)"

profanity - проверка на наличие ненормативной лексики

profanity_check -

streaming -

temperature - Температура выборки. Значение температуры должно быть не меньше ноля. Чем выше значение, тем более случайным будет ответ модели. При значениях температуры больше двух, набор токенов в ответе модели может отличаться избыточной случайностью.

max_tokens - Максимальное количество токенов, которые будут использованы для создания ответов. По умолчанию: 1024

use_api_for_tokens - Используйте GigaChat API для подсчета токенов

verbose - Verbose logging

top_p - Задает вероятностную массу токенов, которые должна учитывать модель. Так, если передать значение 0.1, модель будет учитывать только токены, чья вероятностная масса входит в верхние 10%.

repetition_penalty - Количество повторений слов. 1.0 — нейтральное значение. При значении больше 1 модель будет стараться не повторять слова

update_interval - Минимальный интервал в секундах, который проходит между отправкой токенов
"""

from typing import Optional

from langchain.schema import HumanMessage
from langchain_community.chat_models.gigachat import GigaChat

from GIGAchat.func_config_parser import get_auth


class GigaChatSDK:
    def __init__(
            self,
            model="GigaChat",
            temperature: Optional[float] = None,
            top_p: Optional[float] = None,
            max_tokens: Optional[int] = None,
            repetition_penalty: Optional[float] = None,
            verify_ssl_certs: Optional[bool] = False
    ):

        self.chat = GigaChat(
            credentials=get_auth(),
            model=model,
            verify_ssl_certs=verify_ssl_certs)

        if temperature is not None:
            self.chat.temperature = temperature
        if top_p is not None:
            self.chat.top_p = top_p
        if max_tokens is not None:
            self.chat.max_tokens = max_tokens
        if repetition_penalty is not None:
            self.chat.repetition_penalty = repetition_penalty

    def requestGC(self, event, messages=[]):
        request = f"Тебе нужно придумать описание для события '{event}'в WEB-календаре. Не от первого лица. без упоминания числа. только описание самого события"
        messages.append(HumanMessage(content=request))
        answer = self.chat(messages)
        return answer.content
