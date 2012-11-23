// quickSort.java sorts an array in decreasing order

public class MyArrays {
   public static int[] shellSort(float[] a, int fromIndex, int toIndex) {

       int[] Index = new int[toIndex];
       int d;

      int h = 1; 

      for (int k=0; k<toIndex; k++)
	  Index[k] = k;

      while (h<toIndex-fromIndex) h = 3*h + 1;

      while (h>1) {
         h = h/3;
         for (int i=fromIndex+h; i<toIndex; i++) {
            d = Index[fromIndex+i];
            int j = i; 
            while (j>=fromIndex+h && a[d] < a[Index[fromIndex+j-h]]) {
               Index[fromIndex+j] = Index[fromIndex+j-h];
               j = j - h;
            }
            Index[fromIndex+j] = d;
         }
      }
    return Index;
   }


   public static int[] shellSortDec(float[] a, int fromIndex, int toIndex) {

       int[] Index = new int[toIndex];
       int d;

      int h = 1; 

      for (int k=0; k<toIndex; k++)
	  Index[k] = k;

      while (h<toIndex-fromIndex) h = 3*h + 1;

      while (h>1) {
         h = h/3;
         for (int i=fromIndex+h; i<toIndex; i++) {
            d = Index[fromIndex+i];
            int j = i; 
            while (j>=fromIndex+h && a[d] >= a[Index[fromIndex+j-h]]) {
               Index[fromIndex+j] = Index[fromIndex+j-h];
               j = j - h;
            }
            Index[fromIndex+j] = d;
         }
      }
    return Index;
   }
}

