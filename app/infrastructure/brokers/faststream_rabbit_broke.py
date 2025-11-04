from faststream.rabbit import RabbitBroker

from app.domain.ports.message_broker import IMessageBroker
from app.infrastructure.config.settings import settings


class FastStreamRabbitBroker(IMessageBroker):
    def __init__(self, url: str):
        self._broker = RabbitBroker(url)

    async def start(self):
        """Start the FastStream broker."""
        await self._broker.start()

    async def publish(self, topic: str, message: dict) -> None:
        await self._broker.publish(message, topic)

    async def subscribe(self, topic: str, handler):
        self._broker.subscriber(topic)(handler)

    async def stop(self):
        await self._broker.stop()


broker_service = FastStreamRabbitBroker(settings.rabbitmq_url)
