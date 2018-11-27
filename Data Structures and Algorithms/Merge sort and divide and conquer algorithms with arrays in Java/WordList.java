package testing;

public class WordList {
	
	private int size; //amount of words in array
	private int capacity; //amount of storage in array
	private String [] arr;
	
	//constructor that creates an empty array (all null) with a specified capacity
	public WordList(int capacity)
	{
		this.arr = new String [capacity];
		this.capacity = capacity;
	}
	
	//constructor that takes an input array stores it in the instance array
	//sorts the instance array, then removes duplicates from that instance array
	//and sets the size of the array accordingly
    public WordList(String [] arrayOfWords)
	{
		this.capacity = 2* arrayOfWords.length;
		int i = 0;
		this.arr = new String [this.capacity];
		int high = insertAndCountSize(arrayOfWords); //set size of this.array, input into this arr (includes duplicate values) and get last valid index of arrayOfWords	
		mergeSort(0,high); //sort this.array using mergesort (includes duplicates)
		removeDuplicates(); //removes duplicates
	}
	
	public int getSize()
	{
		return this.size;
	}
	
	public int getCapacity()
	{
		return this.capacity;
	}
	
	//Return word at index i, throws exceptions if i is not a valid index
	public String getWordAt(int i) 
	{
		try
		{
			if(i>=this.size || i<0)
				throw new ArrayIndexOutOfBoundsException();
			else
				return this.arr[i];
		}
		catch(ArrayIndexOutOfBoundsException x)
		{
			System.out.println("Referencing an array with an invalid index (ARRAY INDEX OUT OF BOUNDS)");
			return "Referencing an array with an invalid index (ARRAY INDEX OUT OF BOUNDS)";
		}	
	}
	
	//Checks whether or not the word already is in the array
	//if it is, do nothing, else increase the size of the array
	//then check whether or not the array is full (if so increase capacity
	//of the array) then merge sort the array
	public void insert (String newword)
	{
		int i = 0;
		boolean doInsert = true; //by deault, we would want to insert the new word
		//check if word being added is already in the array
		while (i<this.size)
		{
			//word already exists in the array
			if(newword.compareTo(this.arr[i])==0)
			{
				doInsert = false;
				break;
			}
			i++;
		}
		//word didnt exist in the array
		if(doInsert == true)
		{
			int j=0, temp_size = this.size; // j = index of this.arr, i = index for temp arr
			this.size++;
			
			//current array is full, more space (capacity needs to be allocated)
			if (temp_size == this.capacity)
			{
				String [] temp = this.arr;
				this.capacity = temp_size *2;
				this.arr = new String [this.capacity];
				//store all old array elements in new array
				while(j<temp_size)
				{
					this.arr[j] = temp[j];
					j++;
				}
			}
			//by default, the new word will be inserted into the last position of the array, then sorted
			this.arr[i] = newword;
			mergeSort(0,i);	
		}
	
	}
	
	//used to insert existing String array into instance of arr
	//used when calling the constructor with String array that exists
	//counts the size of the array (includes duplicates)
	private int insertAndCountSize(String [] input)
	{
		int i = 0;
		//loop to count all Strings (inc duplicates) being inserted into instance of arr
		//and count the size of the instance of the arr
		while(i<input.length)
		{
			if(input[i]==null)
				break;
			this.arr [i] = input[i];
			this.size++;
			i++;
		}
		return i-1; //return high index of this.array
	}
	
	//recursive mergeSort algorithm
	private void mergeSort(int low, int high)
	{
		if (low<high)
		{
			int mid = low + (high-low)/2;
			mergeSort(low,mid); //conquer and divide left side of array (of each recursive stack)
			mergeSort(mid+1,high); //conquer and divide right side of array (of each recursive stack)
			merge(low,mid,high); //multiple sorts between array halves
		}
	}
	
	//Removes deplicate Strings (assumes sorted array)
	private void removeDuplicates()
	{
		String [] temp = new String [this.capacity];
		int i = 0,j =0,size=this.size; // to allow loop to loop for full duration (when size for instance array decreases)
		while(i<size)
		{
			//checks previously inserted value, if they are equal
			//skip instance array element when an identical element is found
			if(i>0 && temp[j-1].compareTo(this.arr[i])==0) 
				this.size--;
			else
			{
				temp[j]=this.arr[i];
				j++;
			}
			i++;
		}
		this.arr = temp; //store all changes (array with removed duplicates) in the instance array
	}
	
	//Performs the merge portion of the mergeSort
	private void merge(int low, int mid, int high)
	{
		String [] temp = new String [(high-low)+1];
		int i = low; //used to get specific elements from instance array
		int k = low; //used to place in specific locations of the instance array
		int temp_low = 0; //used to get actual low of the temp array (i.e.: low(i/k) might = 3 or 4 sometimes, but that wouldnt work for temp array - especially at beginning of conquering)
		int temp_high = high-low; //used to get actual high of the temp array (i.e.: high might = 7 or 8 sometimes, but that wouldnt work for temp array - especially at beginning of conquering)
		int temp_mid = temp_low + (temp_high-temp_low)/2;
		int j = temp_mid +1;
		
		//store desired elements from instance array into temp array
		while (temp_low<=(high-low))
		{
			temp[temp_low] = this.arr [i];
			temp_low++;
			i++;
		}
		i=low;
		temp_low = 0;
		
		while(temp_low<=temp_mid && j <=temp_high)
		{
			//higher element comes first
			if(temp[temp_low].compareTo(temp[j])>=0)
			{
				this.arr[k] = temp[j];
				j++;
			}
			else
			{
				//lower element comes first
				if(temp[temp_low].compareTo(temp[j])<=0)
				{
					this.arr[k] = temp[temp_low];
					temp_low++;
				}
			}
			k++;
		}
		
		//unaccounted for lower array elements (within merge)
		if(temp_low<=temp_mid)
		{
			while(temp_low<=temp_mid)
			{
				this.arr[k] = temp[temp_low];
				temp_low++;
				k++;
			}
		}	
		else
		{
			//unaccounted for higher array elements (within merge)
			if(j<=temp_high)
			{
				while(j<=temp_high)
				{
					this.arr[k] = temp[j];
					j++;
					k++;
				}

			}
			
		}
	}
	
	//Finds the word in a list (assumed a sorted list)
	//using divide and conquer (iterative solution)
	public int find(String word)
	{
		int low = 0;
		int high = this.size-1;
		int mid = low + (high-low)/2;
		if(this.size!=0)
		{
			//handle edge cases
			if(word.compareTo(this.arr[low])==0)
				return low;
			if(word.compareTo(this.arr[high])==0)
				return high;
			//divide and conquer loop
			while (low<high)
			{
				if(word.compareTo(this.arr[mid])==0)
					return mid;
				//word is in the upper half of the array
				if(word.compareTo(this.arr[mid])>0)
				{	
					low = mid+1;
					mid = low + (high-low)/2;
				}
				//word is in the lower half of the array
				else
				{
					high = mid;
					mid = low + (high-low)/2;
				}
			}
		}
		return -1; //word is not found
	}
	
	//finds the index belonging to word to be removed
	//then removes the word 
	public void remove (String word)
	{
		int i = find(word);
		if(i!=-1)
		{
			this.arr[i] = this.arr[this.size-1]; // replaces word to be removed with last element
			this.arr[this.size-1] = null; //deletes word by replacing it will null
			this.size--;
		}
		mergeSort(0,this.size-1); //sort array after removal
	}
	
	//create new sublist (WordList object) consisting 
	//of all elements between characters init and fin
	//within the new array. The new capcity alocated is
	//2 * the size of the new array
	public WordList sublist (char init, char fin)
	{
		int j = 0;
		int capacity = 0;
		int size = 0;
		int i = 0;
		while(i<this.size)
		{
			if(this.arr[i].charAt(0)>=init && this.arr[i].charAt(0)<=fin)
				size++;
			i++;
		}
		capacity = size * 2;
		i=0;
		if(size>0)
		{
			WordList list = new WordList(capacity);
			list.size = size;
			while(i<list.size)
			{
				if(this.arr[j].charAt(0)>=init && this.arr[j].charAt(0)<=fin)
				{
					list.arr[i] = this.arr[j];
					i++;
				}
				j++;
			}
			return list;
		}
		else
		{
			WordList list = new WordList(0);
			list.size = 0;
			return list;
		}
	}
			
	//prints out array (with new lines inbetween each element)	
	public String toString()
	{
		String word = "";
		if(this.size == 0)
			 word = "The array wordList is empty";
        else
		{
			word+=this.arr[0];
			int i = 1;
			while(i<this.size)
			{
				word+="\n" + this.arr[i];
				i++;	
			}
		}
        return word;		
	}
}
