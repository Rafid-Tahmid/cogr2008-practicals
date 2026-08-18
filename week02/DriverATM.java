public class DriverATM
{
   public static void main(String[] args)
   {
      SharedAccount sa = new SharedAccount(1000.00);
      SharedAccountClient c1 = new SharedAccountClient(sa);
      SharedAccountClient c2 = new SharedAccountClient(sa);
      double x1 =  100.00;
      double x2 = -100.00;

      c1.setTransaction(x1);
      c2.setTransaction(x2);

      Thread t1 = new Thread(c1);
      Thread t2 = new Thread(c2);
      t1.start();
      t2.start();
   }
}
