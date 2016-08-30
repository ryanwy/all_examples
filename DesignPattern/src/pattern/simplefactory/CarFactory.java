package pattern.simplefactory;

/**
 * Created by Yan on 8/30/2016.
 */
public class CarFactory {
    public static Cars getCar(String name) {
        if (name.equals("bmw")) {
            return new Bmw();
        } else if (name.equals("mazda")) {
            return new Mazda();
        } else {
            return null;
        }
    }
}
