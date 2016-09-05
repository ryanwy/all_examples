package pattern.abstractfactory;

/**
 * Created by Yan on 9/5/2016.
 */
public class ProductMazdaEngine implements IProductEngine {
    @Override
    public void printProduct() {
        System.out.println("Mazda Engine");
    }
}
