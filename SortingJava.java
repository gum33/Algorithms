import java.io.FileReader;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

/* Java practice. Basic sorting implementations, with icelandic comments
sorting implementations for comparable arrays.
Made with help from http://algs4.cs.princeton.edu/home/ 
*/

/*
Glósur í forritunarformi fyri lokapróf í tölvunarfræði 2
nákvæmri comment en má finna í algorithms forritum.
Aukinn skilningur á helstu sort aðferðum. Strengja sort LSD-radix, Robin-Karp
er ekki að finna hér.
*/

public class SortingJava {

private static int length;//Lengd fylkis
private static int i, j, k;//Fyrir lykkjur 
private static Comparable x,y, temp; //Compare x & y, temp fyrir swapping.

	/*Insertion sort N^2/2samanburðir og N^2/2 víxlanir í verst tilviki
	N^2/4 samanburðir og N^2/4 víxlanir að meðaltali
	n-1 samanburðir og engar víxlanir í besta tilvikinu*/
	public static void insertionSort(Comparable[] a) {
		length = a.length;
		/*Insertion sort byrjar á að bera næst fremmsta stak við fremsta stak, því i=0
		fer síðan gegnum fylkið svo lengi sem stakið í sæti i er lægra en stökin á undan*/
		for(i=1;i<length;i++) {
			x=a[i];
			j=i-1;
			/*Swap stak x við það sem er á undan svo lengi sem það er minna
			með compareTo sem skilar neikvæðri tölu ef x<a[j] í þessu tilviki*/
			while(0<=j && x.compareTo(a[j])<0 ) {
				temp = a[j+1];
				a[j+1] = a[j];
				a[j] = temp;
				j--;
			}
		}
	}

	/*Selection sort N^2/2 samanburðir og N víxlanir
	finnur minnsta stakið og setur fremst, svo næst minnsta etc.*/
	public static void selectionSort(Comparable[] a) {
		length = a.length;
		int min;
		/*Lykkja sem finnur minnsta stak til að setja í reit i*/
		for(i=0;i<length;i++) {
			min = i;
			
			/*Lykkja rennur í gegnum allt fylkið eftir i og finnur minnsta stak*/
			for(j=i+1;j<length;j++) {
				if(a[j].compareTo(a[min])<0) {
					min = j;
				}
			}
			//Minnsta stak set í reit i
			if(min != i) {
				temp = a[i];
				a[i] = a[min];
				a[min] = temp;
			}
			 
		}
	}

	/*Merge sort þarf milli (NlogN)/2 og NlogN samanburði og ~6NlogN fylkjaðgerðir
	Fljótari en þarfnast meira minni, set hér fram top-down merge sort
	flóknari en selection og insertion, nota recursive aðferðir.*/
	public static void mergeSort(Comparable[] a) {

		/*Búum til fylki sem er notað til að vista stök úr hlutfylkjum a[]
		þetta er orsök þess að þessi uppsettning mergeSort tekur meira minni en
		aðferðir sem not ekki auka fylki eru talsvert flóknari*/
		Comparable[] copy = new Comparable[a.length]; 
		sortm(a, copy, 0, a.length-1);
	}

	private static void sortm(Comparable[] a, Comparable[] copy, int lo, int hi) {
		if(hi<=lo) return; //Hér er return ef erum komin niðri hlutfylki af engri lengd.

		/* Skiptir fylkjum í tvennt og kallar aftur á þetta fyrir hvern hluta
			Fylkinu er því skipta í marga litla hluta svo er hlutarnir raðaðir og sameinaðir
			hægt að skrifa skilvirkari merge með því að not Insertion Sort á minni hluta fylkjanna
			og gá hvort hlutir séu nú þegar raðaðir, sjá MergeX í princeton.algorithms */

		int mid = lo + (hi - lo) / 2; // Fylki skipt upp
		sortm(a, copy, lo, mid); //fremri hluti
		sortm(a, copy, mid+1, hi); //aftari hluti
		merge(a, copy, lo, mid , hi); // Sameining
	}

	/*Sameinum aftur fylkinn sem búið var að skipta upp */
	private static void merge(Comparable[] a, Comparable[] copy, int lo, int mid, int hi) {

		//Flyjum stök frá a[lo...hi] yfir i copy[]
		for(k=lo; k<=hi ;k++) {
			copy[k] = a[k];
		}

		//Sameining aftir í a[]
		i = lo; 
		j = mid + 1;
		/*
		Hér fyrir stak k í upprunalega fylkinu finnum við hvaða stak úr copy fylkinu við
		viljum setja í a[k].
		*/
		for(k = lo; k<=hi; k++) {
			//Hér væru við komin út í enda fremra fylkis setjum því stök aftari fylkis í a[]
			if 		(i>mid) 						 a[k] = copy[j++];
			//Hér erum við komin út i enda aftari fylkis setjum þvi bara stök fremri fylkis í a[]
			else if (j > hi) 						 a[k] = copy[i++];
			/*Hér berum við saman neðsta stak fremra hlutfylkis og neðsta stak aftari hlutfylkis
			Svo næsta berum við neðsta stak úr því fylki sem var með hærra stak við
			næst neðsta úr því sem var með lægra stak
			förum svo koll af kolli gegnum fylkin*/
			else if (copy[j].compareTo(copy[i]) < 0) a[k] = copy[j++];
			else 								     a[k] = copy[i++];
		}

	}


	/*
	NlogN keyrslutími en er almennt skilvirkara en önnur NlogN reiknirit þar sem meðaltilfellið
	er litli verra en það besta.
	Einnig hægt að kera skilvirkara með að nota insertionsort á lítil hlutfylki og meðhöndla
	jafn stór stök sérstaklega.
	QuickSort skiptir upp safni utan um vendiststak (pivot), skiptir upp safninu utan svo að
	vendisstakið sé á réttum stað. Svo kallað endurkvæmt á það fyrir hvern hluta safnsins.
	*/

	public static void quickSort(Comparable[] a) {
		shuffleArray(a); //Forðumst versta tilvik.
		/* Eins og merge sort viljum við kalla endurkvæmt
		á sortq fyrir a[lo....hi] */
		sortq(a,0,a.length-1);

	}

	/*
	Sjáum að þetta er mjög svipað mergeSort
	hér er endurkvæmt skipt í minni hluta nema ekki í kringum miðju
	heldur kringum vendisstak sem er á búð að setja hærri gildi
	hægra megin við og lægri gildi vinstra megin við
	*/

	public static void sortq(Comparable[] a, int lo, int hi) {
		if(hi <= lo) return; //Hlutsafn orðið 0 í lengd
		int j = partition(a, lo, hi); //Sæti staksins sem við skiptum í kringum
		sortq(a, lo, j-1); //Gildi minni en a[j]
		sortq(a, j+1,hi); //Gildi stærri en a[j]
	}


	/*Skiptum fylkinu upp í a[lo...hi] svo öll stök í a[i..j-1] <=a[j] <=a[j+1..hi]
 	skilum j.
 	Þetta s.s raðar hluta fylkis a sem er frá staki a[lo] a[hi] í kringum eitthvað
 	index j svo öll stök fyrir index < j hafa gildi minna en a[j]
 	og öll stök index > j hafa gildi stærra en a[j] skilum j
 	svo er kallað endurkvæmt svo öll hlutfylki raðast */
	public static int partition(Comparable[] a, int lo, int hi) {
		i = lo;
		j= hi+1;
		x = a[lo];
		while(true) {

			//Finnum stak í lo sem er hærra en x til að setja aftar
			while(a[++i].compareTo(x)<0)
				if (i == hi) break;

			//Finnum stak í hi sem er lægra en x og setjum framan
			while(x.compareTo(a[--j])<0)
				if(j==lo) break;

			if(i>=j) break;

			swap(a, i , j); //swap á gildi í stökum a[i] og a[j]
		}

		//set gildi a[j] á réttan stað
		swap(a,lo, j);

		//Nú eru gildi í a[lo....j-1] <= a[j] og gildi a[j] <= a[j+1....hi]
		//Skilun pivot
		return j;
	}

	private static void swap(Comparable[] a, int lo, int pivot) {
		temp = a[lo];
		a[lo] = a[pivot];
		a[pivot] = temp;
	}

	/***
	Aðferð til að gá hvort fylki er sorted
	**/
	private static boolean isSorted(Comparable[] a) {
		return isSorted(a, 0, a.length-1);
	}

	private static boolean isSorted(Comparable[] a, int lo, int hi) {
		for(int i = lo +1;i <= hi; i++)
			if(a[i].compareTo(a[i-1])<0) return false;
		return true;
	}



	/*****
	Fisher-Yates stokkun, notað í prófun og í quicksort
	http://stackoverflow.com/a/1520212
	*/

	private static void shuffleArray(Comparable[] ar) {
	    Random rnd = ThreadLocalRandom.current();
	    for (int i = ar.length - 1; i > 0; i--) {
	      int index = rnd.nextInt(i + 1);
	      //swap
	      Comparable a = ar[index];
	      ar[index] = ar[i];
	      ar[i] = a;
	    }
	  }




	/* 
	Nota 50.000 stök úr
	http://algs4.cs.princeton.edu/14analysis/1Mints.txt
	til prufunar.
	Þarf að breya ef á að reyna eitthvað annað en 1Mints.txt*/
	public static void main(String[] args) {
		Integer[] array = new Integer[50000];

		try {
			Scanner scanner = new Scanner(new FileReader("1Mints.txt"));

			for(i=0;i<array.length;i++) {
				Integer iInteger =  scanner.nextInt();
				array[i] = iInteger;
			}

			shuffleArray(array);
			mergeSort(array);
			System.out.println(isSorted(array));

			shuffleArray(array);
			selectionSort(array);
			System.out.println(isSorted(array));

			shuffleArray(array);
			insertionSort(array);
			System.out.println(isSorted(array));

			shuffleArray(array);
			quickSort(array);
			System.out.println(isSorted(array));
		}

		catch (FileNotFoundException e) {
			throw new IllegalArgumentException("Vantar 1Mints.txt skjalid");
		}
	}
}