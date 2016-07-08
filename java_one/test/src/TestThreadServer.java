import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Set;



public class TestThreadServer {
    private int port = 8001;
    private String ipAddress = "0.0.0.0";
    private Selector selector;
    private final int BLOCK = 1024;
    private ByteBuffer readBuffer;
    private ByteBuffer writeBuffer;
    private List<SocketChannel> scList;

    public TestThreadServer(String address, int port) throws IOException {
        this.port = port;
        this.ipAddress = address;
        readBuffer = ByteBuffer.allocate(this.BLOCK);
        writeBuffer = ByteBuffer.allocate(this.BLOCK);
        scList = new ArrayList<SocketChannel>();
    }

    public void init() throws IOException {
        ServerSocketChannel serverChannel = ServerSocketChannel.open();
        serverChannel.configureBlocking(false);

        ServerSocket serverSocket = serverChannel.socket();
        serverSocket.bind(new InetSocketAddress(this.ipAddress, this.port));

        this.selector = Selector.open();
        serverChannel.register(selector, SelectionKey.OP_ACCEPT);
        new Thread(new ThreadHandleWrite()).start(); // new thread
        listenConnect();
    }

    private class ThreadHandleWrite implements Runnable{
        public void run() {
            while (true) {
                try {
                    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
                    String text = "Server: " + br.readLine();
                    if (text.length() > "Server: ".length() && !scList.isEmpty()) {
                        SocketChannel sc = scList.get(0);
                        if(!sc.isConnected()) {
                            continue;
                        }
                        writeBuffer.clear();
                        writeBuffer.put(text.getBytes());
                        writeBuffer.flip();
                        sc.write(writeBuffer);
                    }
                } catch (IOException io) {
                    System.out.println(io.getMessage());
                }
            }
        }
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
                    System.out.println("get new connection: " + socketChannel.getRemoteAddress().toString());
                    writeBuffer.clear();
                    String serverMessage = "Welcome, this is " + InetAddress.getLocalHost().getHostAddress();
                    writeBuffer.put(serverMessage.getBytes());
                    writeBuffer.flip();
                    socketChannel.write(writeBuffer);
                    scList.add(socketChannel);
                    socketChannel.register(this.selector, SelectionKey.OP_READ);
                } else if(key.isReadable()) {
                    socketChannel = (SocketChannel)key.channel();
                    readBuffer.clear();
                    count = socketChannel.read(readBuffer);
                    String strBuffer;
                    if(count > 0) {
                        strBuffer = new String(readBuffer.array(), 0, count);
                        System.out.println(strBuffer);
                    }
                    // socketChannel.register(this.selector, SelectionKey.OP_WRITE);
                }/* else if(key.isWritable()) {
                    writeBuffer.clear();
                    socketChannel = (SocketChannel)key.channel();
                    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
                    String text = "Server: " + br.readLine();
                    writeBuffer.put(text.getBytes());
                    writeBuffer.flip();
                    socketChannel.write(writeBuffer);
                    socketChannel.register(this.selector, SelectionKey.OP_READ);
                } else {
                    System.out.println("what's wrong");
                } */
                iterator.remove();
            }

        }
    }

}
