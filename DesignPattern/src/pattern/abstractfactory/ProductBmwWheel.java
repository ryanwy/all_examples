package pattern.abstractfactory;

/**
 * Created by Yan on 9/5/2016.
 */
public class ProductBmwWheel implements IProductWheel {
    @Override
    public void printProduct() {
        System.out.println("BMW Wheel");
    }
}
