import discord
from discord.ext import commands
from discord.commands import Option, OptionChoice, SlashCommandGroup
import json

# クローラーを実行する関数
async def crawler(guild: discord.Guild, is_reverse: bool = True):
    categories = []
    channels = []
    messages = []
    count = 1
    # チャンネルのカテゴリーをすべて取得
    for category in guild.categories:
        # カテゴリー内がすべてボイスチャンネルの場合は除外
        if len(category.text_channels) != 0:
            categories.append({"category_id": category.id, "name": category.name})
    
    # サーバー内のチャンネル一覧のidと名前を表示
    for channel in guild.channels:
        # テキストチャンネルのみを抽出
        if isinstance(channel, discord.TextChannel):
            # channelのリストに追加
            channels.append({"category_id": channel.category_id, "channel_id": channel.id, "name": channel.name})      
        
            # メッセージのアーカイブを作成
            async for message in channel.history(limit=None):
                if count % 1000 == 0:
                    print(f"進捗: {channel.name} -> {count}")
                messages.append(
                    {
                        "channel_id": message.channel.id,
                        "author_id": message.author.id,
                        "author": message.author.name,
                        "content": message.content,
                        "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
                count += 1
        
    # _categories.jsonを作成
    with open(f"history/_categories.json", "w") as f:
        json.dump(categories, f, indent=4, ensure_ascii=False)
    
    # channels.jsonを作成
    with open(f"history/_channels.json", "w") as f:
        json.dump(channels, f, indent=4, ensure_ascii=False)

    # messagesの順番を逆転させる
    if is_reverse:
        messages.reverse()
    with open(f"history/{channel.id}.json", "w") as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)
    print(f"{channel.name}のメッセージを保存しました -> {count-1} messages({channel.id}.json)")


class Crawler():
    async def all_channel(
        self,
        guild: discord.Guild,
        is_reverse: bool = True,
    ):
        print("クロール対象のチャネル一覧を表示します")
        channels = await guild.fetch_channels()

        # textチャネルのみを抽出
        channels = [channel for channel in channels if isinstance(
            channel, discord.TextChannel)]

        # チャネル名を表示
        channel_names = [channel.name for channel in channels]
        print("\n".join(channel_names))

        # チャネルごとの過去のメッセージをファイルに保存
        for channel in channels:
            print(f"{channel.name}のメッセージを保存します")
            await crawler(guild, is_reverse)
        print("クロールを終了します")
        
        return True
