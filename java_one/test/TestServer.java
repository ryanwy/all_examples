import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.nio.charset.Charset;
import java.util.Iterator;
import java.util.Set;


public class TestServer {
    private int port = 8001;
    private String ipAddress = "0.0.0.0";
    private Selector selector;
    private final int BLOCK = 1024;
    private ByteBuffer readBuffer;
    private ByteBuffer writeBuffer;

    public TestServer(String address, int port) throws IOException {
        this.port = port;
        this.ipAddress = address;
        readBuffer = ByteBuffer.allocate(this.BLOCK);
        writeBuffer = ByteBuffer.allocate(this.BLOCK);
    }

    public void init() throws IOException {
        ServerSocketChannel serverChannel = ServerSocketChannel.open();
        serverChannel.configureBlocking(false);

        ServerSocket serverSocket = serverChannel.socket();
        serverSocket.bind(new InetSocketAddress(this.ipAddress, this.port));

        this.selector = Selector.open();
        serverChannel.register(selector, SelectionKey.OP_ACCEPT);
        listenConnect();
    }

    private void listenConnect() throws IOException {
        ServerSocketChannel serverSocketChannel = null;
        SocketChannel socketChannel = null;

        while(true) {
            this.selector.select();
            Set selectorKeys = this.selector.selectedKeys();
            Iterator iterator = selectorKeys.iterator();
            int count = 0;

            while(iterator.hasNext()) {
                SelectionKey key = (SelectionKey) iterator.next();

                if(key.isAcceptable()) {
                    serverSocketChannel = (ServerSocketChannel)key.channel();
                    socketChannel = serverSocketChannel.accept();
                    socketChannel.configureBlocking(false);
                    socketChannel.register(this.selector, SelectionKey.OP_WRITE);
                    System.out.println("get new connection: " + socketChannel.getRemoteAddress().toString());
                } else if(key.isReadable()) {
                    socketChannel = (SocketChannel)key.channel();
                    readBuffer.clear();
                    count = socketChannel.read(readBuffer);
                    String strBuffer;
                    if(count > 0) {
                        strBuffer = new String(readBuffer.array(), 0, count);
                        System.out.println(strBuffer);

                    }
                    //socketChannel.register(this.selector, SelectionKey.OP_WRITE);
                } else if(key.isWritable()) {
                    writeBuffer.clear();
                    socketChannel = (SocketChannel)key.channel();
                    String text = "hello, this is server";
                    writeBuffer.put(text.getBytes());
                    writeBuffer.flip();
                    socketChannel.write(writeBuffer);
                    socketChannel.register(this.selector, SelectionKey.OP_READ);
                } else {
                    System.out.println("what's wrong");
                }
                iterator.remove();
            }

        }
    }

}
