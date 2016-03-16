public class QuickSortDemo {
	public static void main(String args[]) {
		int data[] = new int[]{9,5,6,4,1,2,3,7,0};
		print(data);
		quicksort(data);
		print(data);
	}

	public static void print(int arr[]) {
		for(int i=0; i<arr.length; i++) {
			System.out.print(arr[i] + "、");
		}
		System.out.println();
	}

	public static int partition(int arr[], int lo, int hi) {
		int i = lo;
		int j = hi + 1;
		while(true) {
			i++;
			while(arr[i] < arr[lo]) {
				if(i == hi) {
					break;
				}
				i++;
			}
			j--;
			while(arr[j] > arr[lo]) {
				if(j == lo) {
					break;
				}
				j--;
			}
			if (i >= j) {
				break;
			}
			int t = arr[i];
			arr[i] = arr[j];
			arr[j] = t;
		}
		int t = arr[lo];
		arr[lo] = arr[j];
		arr[j] = t;
		return j;
	}

	public static void sort(int arr[], int lo, int hi) {
		if(lo >= hi) {
			return;
		}
		int index = partition(arr, lo, hi);
		sort(arr, lo, index-1);
		sort(arr, index+1, hi);
	}

	public static void quicksort(int arr[]) {
		sort(arr, 0, arr.length-1);
	}

}
