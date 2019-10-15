import asyncio
import socket
import shutil

checked = 0
cols = shutil.get_terminal_size().columns

async def check(host, port, opened):
    global checked, cols
    sock = socket.socket()
    try:
        await sock.connect((host, port))
    except OSError:
        pass
    except TypeError:
        # TypeError выбрасывается, когда в await возвращается открытый connection => порт открыт
        # print('Порт {} открыт'.format(port))
        opened.append(port)
    finally:
        print('#' * int(checked / 65536 * cols))
        checked += 1
        sock.close()

async def main():
    host = input('Host: ') or 'localhost'
    opened = []
    futures = [check(host, i, opened) for i in range(65536)]
    await asyncio.wait(futures)
    print('Открытые порты: {}'.format(sorted(opened)))

asyncio.run(main())
