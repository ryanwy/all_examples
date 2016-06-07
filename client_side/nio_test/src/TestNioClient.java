import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

public class TestNioClient {

	public String m_strIpAddress;
	public int m_iPort;

	private Selector selector;
	
	public void init_client() throws IOException {
		SocketChannel socketChannel = SocketChannel.open();
		socketChannel.configureBlocking(false);
		socketChannel.socket().bind(new InetSocketAddress(this.m_iPort));
        this.selector = Selector.open();
        socketChannel.connect(new InetSocketAddress(this.m_strIpAddress, this.m_iPort));
        socketChannel.register(this.selector, SelectionKey.OP_CONNECT);
		return;
	}
	
	public void listen_client() throws IOException {
		while(true) {
			selector.select();
			Iterator<SelectionKey> iterator = this.selector.selectedKeys().iterator();
			while(iterator.hasNext()) {
				SelectionKey key = (SelectionKey)iterator.next();
				iterator.remove();
				
				if (key.isConnectable()) {
					SocketChannel channel = (SocketChannel)key.channel();
                    if(channel.isConnectionPending()) {
                        channel.finishConnect();
                    }  
                    channel.configureBlocking(false);
					channel.write(ByteBuffer.wrap(new String("Connected").getBytes()));
					channel.register(this.selector, SelectionKey.OP_READ);
				} else if (key.isReadable()) {
					read_client(key);
				} else if (key.isWritable()) {
					write_client(key);
				}
			}
		}
	}
	
	private void read_client(SelectionKey key) throws IOException {
		SocketChannel channel = (SocketChannel)key.channel();
		ByteBuffer buffer = ByteBuffer.allocate(20);
		channel.read(buffer);
		byte[] data = buffer.array();
		String msg = new String(data).trim();
		System.out.println("Client received:");
		System.out.println(msg);
		channel.register(this.selector, SelectionKey.OP_WRITE);
		return;
	}
	
	private void write_client(SelectionKey key) throws IOException {
		SocketChannel channel = (SocketChannel)key.channel();
		ByteBuffer buffer = ByteBuffer.allocate(20);
		buffer.put(new String("This is client").getBytes());
		buffer.flip();
		channel.write(buffer);
		// System.out.println("Send to server");
		// channel.register(this.selector, SelectionKey.OP_READ);
		return;
	}
}
