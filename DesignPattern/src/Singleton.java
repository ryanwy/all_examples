/**
 * Created by Yan on 8/30/2016.
 * 单例模式，创建型模式，是23种设计模式之一，确保一个类只有一个实例，应用场景为资源共享和控制资源
 * 优点：内存中只存在一个对象，节约系统资源；受控访问；
 * 缺点：无抽象层，难以扩展；
 * 以下提供两种懒汉lazy和饿汉hungry模式的例子
 */
public class Singleton {
//    This is Singleton example - lazy
//    private static Singleton st = null;
//
//    private Singleton() {
//
//    }
//
//    public static synchronized Singleton getInstance() {
//        if( null == st ) {
//            st = new Singleton();
//        }
//        return st;
//    }

    // Singleton example - hungry
    private final static Singleton st = new Singleton();
    private Singleton() {

    }
    public static Singleton getInstance() {
        return st;
    }

    public static void main(String[] args) throws Exception {
        Singleton st = Singleton.getInstance();
        System.out.println(st);
    }
}
