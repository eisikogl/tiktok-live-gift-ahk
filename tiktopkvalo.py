import asyncio, sys
from ahk import AHK
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent,LikeEvent
import time

# Instantiate AHK
ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')

async def process_chat():
    while True:
        await asyncio.sleep(1)

async def main():
    # Instantiate the client with the user's username
    client = TikTokLiveClient(unique_id="@caliongames", enable_detailed_gifts=True)

    # Define how to handle specific events via decorator
    @client.on("connect")
    async def on_connect(_: ConnectEvent):
        print("Connected to Room ID:", client.room_id)
    
    @client.on("like")
    async def on_like(event: LikeEvent):
        print(f"@{event.user.unique_id} liked the stream!")
        ahk.click()

    async def click_screen(ahk):
        await ahk.run_script('Click')
    @client.on("gift")
    async def on_gift(event: GiftEvent):
        print(f"{event.user.unique_id} sent {event.gift.count}x \"{event.gift.info.name}\"")
        if  1 <= event.gift.info.diamond_count <= 4:
            ahk.click()
            print("CLICKED")
        elif 5 <= event.gift.info.diamond_count <= 9:
            ahk.key_press('3')
            print("3 pressed")
        elif 10 <=event.gift.info.diamond_count <= 19:
            ahk.key_press('Space')
            print("space pressed")
        elif 20 <= event.gift.info.diamond_count <= 29:
            ahk.key_press('g')
            print("gun dropped")
        elif 30 <= event.gift.info.diamond_count <= 49:
            ahk.key_press('x')
            ahk.click()
            print("ulti activated")
        elif 50 <= event.gift.info.diamond_count <= 99:
            ahk.key_down('Control')
            print("crouching 10 sec")
            time.sleep(10)
            ahk.key_up('Control')
            print("crouched 10 sec")
        elif event.gift.info.diamond_count >= 100:
            ahk.key_down('s')
            print("walking backwards")
            time.sleep(60)
            ahk.key_up('s')
            print("walking backwards end")
 #   @client.on("comment")
#    async def on_comment(event: CommentEvent):
#        print(f"{event.user.nickname} -> {event.comment}")


    try:
        # Start the client without blocking the main thread
        await client.start()

        # Run the chat processing in the background
        await process_chat()

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) gracefully
        print("Interrupted")
    finally:
        # Stop AHK when exiting the program
        # It should be ahk.stop() not ahk.Stop()
        pass
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(main())
