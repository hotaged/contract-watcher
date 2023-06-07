import click

from functools import wraps
from tortoise import Tortoise, run_async

from contract_watcher.config import TORTOISE_ORM
from contract_watcher.models import User


@click.group()
def cli():
    pass


def coro(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        run_async(f(*args, **kwargs))

    return wrapper


@click.command('create-user')
@click.option("--username", '-u', required=True, type=str)
@click.option("--password", '-p', required=True, type=str)
@coro
async def create_user(username: str, password: str):
    await Tortoise.init(config=TORTOISE_ORM)

    if not await User.exists(username=username):
        await User.create_with_encrypted_password(username, password)

        click.secho(f"Successfully created user: {username}", fg='green')

    else:
        click.secho(f"User with the given username already exists: {username}", fg='yellow')


@click.command('update-user-password')
@click.option("--username", '-u', required=True, type=str)
@click.option("--password", '-p', required=True, type=str)
@coro
async def update_user_password(username: str, password: str):
    await Tortoise.init(config=TORTOISE_ORM)

    if await User.exists(username=username):
        user = await User.get(username=username)
        await user.change_password(password)

        click.secho(f"Successfully update user password: {username}", fg='green')

    else:
        click.secho(f"User with the given username does not exists: {username}", fg='yellow')


@click.command('delete-user')
@click.option("--username", '-u', required=True, type=str)
@coro
async def delete_user(username: str | None):
    await Tortoise.init(config=TORTOISE_ORM)

    if await User.exists(username=username):
        user = await User.get(username=username)
        await user.delete()

        click.secho(f"Successfully deleted user password: {username}", fg='green')

    else:
        click.secho(f"User with the given username does not exists: {username}", fg='yellow')


cli.add_command(create_user)
cli.add_command(update_user_password)
cli.add_command(delete_user)

