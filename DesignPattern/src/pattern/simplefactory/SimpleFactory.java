package pattern.simplefactory;

/**
 * Created by Yan on 8/30/2016.
 * 简单工厂模式，创建型模式，不属于23种Gof设计模式。可以看出简单工厂的组成 client---工厂----抽象接口----产品实现
 * 优点：工厂类是简单工厂模式的核心，隔离了了客户端和底层的具体实现，只需要一定的信息就可以了就可以获得特定的产品，而不必关心具体的对象创建
 * 缺点：逻辑判断过度集中在工厂类中，不利于扩展，每次修改还要修改工厂类，而且不便于维护
 * 应用场景：适合于负责创建对象比较少的情景；客户只传入参数，对于具体创建什么对象并不关心
 *
 * 简单工厂模式中，无论是宝马还是马自达都是一个工厂生产出来的，而如果想新增一个品牌比如福特，还需要修改工厂类，这样就违反了开放封闭原则（对扩展
 * 开放，对修改是封闭的）；软件设计的目标是封闭变化，降低耦合，应该是可扩展，而不可修改的
 */
public class SimpleFactory {
    public static void main(String[] args) throws Exception {
        Cars car = CarFactory.getCar("bmw");
        car.printStyle();
        Cars car2 = CarFactory.getCar("mazda");
        car2.printStyle();
    }
}
