from discord.mixins import Hashable
from discord.member import Member
from discord.message import Message
from discord.utils import snowflake_time


class Interaction(Hashable):
    def __init__(self, *, state, channel, guild, data):
        self._state = state
        self.id = int(data['id'])
        self.type = int(data['type'])
        self.token = data['token']
        self.version = int(data['version'])
        self.channel, self.guild = channel, guild
        self.member = Member(data=data['member'], state=self._state, guild=self.guild)
        self.data = data['data']
        if 'options' in self.data:
            print(self.data['options'])  # TODO: Print

    def __repr__(self):
        return '<Interaction id={0.id} channel={0.channel!r} type={0.type!r} member={0.member!r}>'.format(self)

    @property
    def created_at(self):
        """:class:`datetime.datetime`: The message's creation time in UTC."""
        return snowflake_time(self.id)

    async def ack(self, with_source=True):
        t = 5 if with_source else 2
        return await self._state.http.send_interaction_response(self.id, self.token, t)

    async def send(self, content=None, with_source=True, **kwargs):
        if 'embed' in kwargs:
            kwargs['embed'] = kwargs['embed'].to_dict()
        t = 4 if with_source else 3
        data = await self._state.http.send_interaction_response(self.id, self.token, t, content, **kwargs)

    async def delete(self):  # TODO
        pass
