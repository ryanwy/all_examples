import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

/*
 * for nio server
 */
public class TestNioServer {
	
	public int m_iPort;
	private Selector selector;
	
	public void init_server() throws IOException {
		// open a socket channel
		ServerSocketChannel serverChannel = ServerSocketChannel.open();
		// configure as non-block
		serverChannel.configureBlocking(false);
		// bind ip and port
		serverChannel.socket().bind(new InetSocketAddress("0.0.0.0", this.m_iPort));
        this.selector = Selector.open();
        // register to selector
		serverChannel.register(this.selector, SelectionKey.OP_ACCEPT);
		return;
	}
	
	
	public void listen_server() throws IOException {
		while(true) {
			// select a set of keys
			this.selector.select();
			// loop for check status
			Iterator<SelectionKey> iterator = this.selector.selectedKeys().iterator();
			while(iterator.hasNext()) {
				SelectionKey key = (SelectionKey)iterator.next();
				iterator.remove();
				// check is accept or read or write
				if (key.isAcceptable()) {
				    ByteBuffer buffer = ByteBuffer.allocate(20);	
                    ServerSocketChannel server = (ServerSocketChannel)key.channel();
					SocketChannel channel = server.accept();
					channel.configureBlocking(false);
                    buffer.put(new String("New connection").getBytes());
					channel.write(buffer);
                    // buffer.clear();
					channel.register(this.selector, SelectionKey.OP_READ);
				} else if(key.isReadable()) {
					read_server(key);
				} else if(key.isWritable()) {
					write_server(key);
				}
			}
		}
	}
	
	private void read_server (SelectionKey key) throws IOException {
		SocketChannel channel = (SocketChannel)key.channel();
		ByteBuffer buffer = ByteBuffer.allocate(20);
		channel.read(buffer);
		byte[] data = buffer.array();
		String msg = new String(data).trim();
		System.out.println("Server received:");
		System.out.println(msg);
		buffer.clear();
		channel.register(this.selector, SelectionKey.OP_WRITE);
		return;
	}
	
	private void write_server(SelectionKey key) throws IOException {
		SocketChannel channel = (SocketChannel)key.channel();
		ByteBuffer buffer = ByteBuffer.allocate(20);
		buffer.put(new String("This is server").getBytes());
		buffer.flip();
		channel.write(buffer);
		// System.out.println("Send to client");
		// channel.register(this.selector, SelectionKey.OP_READ);
		return;
	}
}
