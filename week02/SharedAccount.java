public class SharedAccount
{
   private double balance;

   public SharedAccount(double initialAmount)
   {
      balance = initialAmount;
   }

   public synchronized void completeTransaction(double amount)
   {
      double temp = this.balance + amount;

      if (amount < 0) {
         System.out.println("Withdraw: old balance = " + balance);
         System.out.println("Withdraw: amount = " + Math.abs(amount));
      }
      else {
         System.out.println("Deposit: old balance = " + balance);
         System.out.println("Deposit: amount = " + Math.abs(amount));
      }


      try
      {
         Thread.sleep(1000);
      }
      catch (InterruptedException e)
      {
         System.out.println("Transaction interrupted.");
      }

      balance = temp;

      if (amount < 0) {
         System.out.println("Withdraw: new balance = " + balance);
      }
      else {
         System.out.println("Deposit: new balance = " + balance);
      }
   }
}
