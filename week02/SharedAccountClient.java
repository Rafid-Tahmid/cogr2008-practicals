public class SharedAccountClient implements Runnable
{
   double transaction;
   SharedAccount sa;

   public SharedAccountClient(SharedAccount sa)
   {
      this.sa = sa;
   }

   public void setTransaction(double transaction)
   {
      this.transaction = transaction;
   }

   public void run()
   {
      sa.completeTransaction(transaction);
   }
}
