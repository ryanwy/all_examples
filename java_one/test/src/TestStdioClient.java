import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
import java.util.Set;


public class TestStdioClient {
    private String serverIpAddress = "";
    private int port = 0;
    private Selector selector = null;
    private final int BLOCK = 1024;
    private ByteBuffer readBuffer = null;
    private ByteBuffer writeBuffer = null;


    public TestStdioClient(String serverIp, int port) {
        this.serverIpAddress = serverIp;
        this.port = port;
        this.readBuffer = ByteBuffer.allocate(BLOCK);
        this.writeBuffer = ByteBuffer.allocate(BLOCK);
    }

    public void init() throws IOException {
        SocketChannel socketChannel = SocketChannel.open();
        socketChannel.configureBlocking(false);

        this.selector = Selector.open();
        socketChannel.register(this.selector, SelectionKey.OP_CONNECT);
        socketChannel.connect(new InetSocketAddress(this.serverIpAddress, this.port));
        handleOperation();
    }

    private void handleOperation() throws IOException {
        SocketChannel socketChannel = null;

        while(true) {
            this.selector.select();
            Set selectorKeys = this.selector.selectedKeys();
            Iterator iterator = selectorKeys.iterator();
            int count = 0;

            while(iterator.hasNext()) {
                SelectionKey key = (SelectionKey)iterator.next();
                if(key.isConnectable()) {
                    socketChannel = (SocketChannel)key.channel();
                    if(socketChannel.isConnectionPending()) {
                        socketChannel.finishConnect();
                        writeBuffer.clear();
                        String message = "hello, this is client";
                        writeBuffer.put(message.getBytes());
                        writeBuffer.flip();
                        socketChannel.write(writeBuffer);
                    }
                    socketChannel.register(this.selector, SelectionKey.OP_READ);
                } else if(key.isReadable()) {
                    socketChannel = (SocketChannel)key.channel();
                    readBuffer.clear();
                    String strBuffer;
                    count = socketChannel.read(readBuffer);
                    if (count > 0) {
                        strBuffer = new String(readBuffer.array(), 0, count);
                        System.out.println(strBuffer);
                    }

                    socketChannel.register(this.selector, SelectionKey.OP_WRITE);
                } else if(key.isWritable()) {
                    writeBuffer.clear();
                    socketChannel = (SocketChannel)key.channel();
                    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
                    String text = "Client: " + br.readLine();
                    writeBuffer.put(text.getBytes());
                    writeBuffer.flip();
                    socketChannel.write(writeBuffer);
                    socketChannel.register(this.selector, SelectionKey.OP_READ);
                } else {
                    System.out.println("oh, anything wrong?");
                }
                iterator.remove();
            }

        }
    }
}
