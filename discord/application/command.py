"""
The MIT License (MIT)

Copyright (c) 2021-present Texus

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio
import types
from discord.types.channel import VoiceChannel, TextChannel
import functools
import inspect
from collections import OrderedDict
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union
)

from ..enums import SlashCommandOptionType, ChannelType
from ..member import Member
from ..user import User
from ..message import Message
from .context import ApplicationContext
from ..utils import find, get_or_fetch, async_all

from ..errors import DiscordException, NotFound, ValidationError, ClientException
from .errors import ApplicationCommandError, CheckFailure, ApplicationCommandInvokeError

def wrap_callback(coro):
    @functools.wraps(coro)
    async def wrapped(*args, **kwargs):
        try:
            ret = await coro(*args, **kwargs)
        except ApplicationCommandError:
            raise
        except asyncio.CancelledError:
            return
        except Exception as exc:
            raise ApplicationCommandInvokeError(exc) from exc
        return ret
    return wrapped

def hooked_wrapped_callback(command, ctx, coro):
    @functools.wraps(coro)
    async def wrapped(arg):
        try:
            ret = await coro(arg)
        except ApplicationCommandError:
            raise
        except asyncio.CancelledError:
            return
        except Exception as exc:
            raise ApplicationCommandInvokeError(exc) from exc
        finally:
            await command.call_after_hooks(ctx)
        return ret
    return wrapped

class _BaseCommand:
    __slots__ = ()

class ApplicationCommand(_BaseCommand):
    # TODO: Implement application commands
    raise NotImplementedError