/*
Alexander Szebrag 
Lab Section 03
1148394
Lab 01

 */
package laab1;

public class WordList 
{
    private int size;
    private int capacity;
    private String [] a= new String [capacity];
    
    public WordList(int capacity)
    {
       //no need to update size, as every element is null 
        this.capacity=capacity;//initializes this capacity to the value passed
        this.size=0;//not neccesary
        String [] a = new String [this.capacity];//creates new array of strings
        this.a=a;//private variable references newly created array(new list)
        int i=0;
        while(i<capacity)
        {
            this.a[i]=null;//initializing all elements to null
            i++;
        }
        
    }
    
            
    public WordList(String [] arrayOfWords)
    {
        int len=arrayOfWords.length,i=0,j=0;
        this.capacity=arrayOfWords.length*2;//capacity of new wordlist object initialized to twice the size of the original array
        String temp;
        //FIRST PORTION: (2 loops deals with sorting the passed array)
        while(i<len)//loop to go through the array (used to get the effective size of the list, and sort the array alphabetically)
        {
            while(j<len)
          {
              if(arrayOfWords[j]==null)//if the element is null
              {
                  j++;
                  continue;
              }
            if(arrayOfWords[i].compareTo(arrayOfWords[j])>0&&i<j)//compares the ith element in the array to every element after the ith element. (word[i] comes after word[j] alpabetically)
            {
                //swaps the ith element with the jth element, where the jth element is always greater(in terms of index) than the ith element
                //jth element is smaller alphabetically than the ith element
                temp=arrayOfWords[i];//temperarly stores the ith element (so its not lost)
                arrayOfWords[i]=arrayOfWords[j];//replaces ith element with jth element
                arrayOfWords[j]=temp;//swap of jth element with ith element
                i=0;//restarts the ith element so that every element is recompared with the first element 
                
            }
            else
            {
                if(arrayOfWords[i].compareTo(arrayOfWords[j])==0&&i<j)//situation where two words are equal
                {
                    temp=arrayOfWords[len-1];//so that last word in the list is not lost.
                    arrayOfWords[j]=temp;// It replaces the repeated word with the last word in the list
                    arrayOfWords[len-1]= null;//makes the last element null, effectively removing an element
                    len--;//effective size of list is decremented, 1 less element to check (loop condition)
                    i=0;//restarts the ith element so that every element is recompared with the first element 
                }
                else
                {
                    if(arrayOfWords[i].compareTo(arrayOfWords[j])<0 &&i<j)//situation where no swap occurs cause word[i]comes before word][j] alphabetically
                    {
                        j++;//so that ith element is compared with the next element
                        continue;//continue through second loop
                    
                    }        
                 }
            
            }
            j++;
          }
            j=0;//so that second loop will keep running until every ith element has been compafred
            i++;
            
        }
        //this.capacity=2*len;//capacity=twice the size of the array
        //SECOND PORTION: deals with creating the list and adding the elements
        this.size=len;//makes size of list equal to the effective length found by going through the 2 loops (used to elimimate 2 identicle elements)
        String [] a = new String [this.capacity];//created array of strings equal to original size of the array(before identical elements are eliminated)
        this.a=a;//makes list reference newly created array of strings
        i=0;
        int length=arrayOfWords.length;//makes length equal to the length of the array after removal of identical elements
        while(i<this.capacity)
        {
            if(i>=length)//elements after the effecitve size of the list are initialized to null
                this.a[i]=null;
            else
                this.a[i]=arrayOfWords[i];//initializes private string array to the words of the array 
            i++;
            
        }
       
    }
    public int getSize()
    {
        return size;
    }
    public int getCapacity()
    {
        return capacity;
    }
    public String getWordAt(int i)
    {
        if(i<size && i>=0)//if its a valid index (0-size-1), itll return the word at index
            return a[i];
        else//throws an exception if its out of bounds
            throw new ArrayIndexOutOfBoundsException("This index is not valid!");            
    }
    public void insert(String newword)
    {
        int i=0,j=0,k=0,l=0,pos=-1;//pos is the index where the new word should be inserted
        while(i<size)//loop to detrmine if the word is already in the list
        {
            
            if(a[i].compareTo(newword)==0)
            {   l=-1;//variable used to indicate that the word is already in the list(set to -1 if already in list)
                break;
            }
            i++;
        }
        if(a[0]==null || size<=1)//due to my loop condition later (<size-1), i need this condtion to solve for lists that have 0-1 elements in them
        {
            if(a[0]==null)//enters if empty list
            {
                a[0]=newword;//adds element to an empty list
                l=-1;//variable used to indicate that the word is already in the list(set to -1 if already in list)
                this.size+=1;//increases list size
            }
            else//enters for a list with 1 word
            {
                if(a[0].compareTo(newword)<0)//new word comes after the word already in list
                {
                    a[1]=newword;
                    l=-1;//variable used to indicate that the word is already in the list(set to -1 if already in list)
                    this.size+=1;
                }
                else//new word comes before word already in list
                {
                    if(a[0].compareTo(newword)>0)
                    {
                        String temp3="";//temp varaiable used to store contents of 1st element
                        temp3=a[0];
                        a[0]=newword;
                        a[1]=temp3;
                        l=-1;//variable used to indicate that the word is already in the list(set to -1 if already in list)
                        this.size+=1;
                    }
                    
                }
                
            }
        }
        if(l!=-1 && a[0]!=null&&size>1)//if not repeated word and for cases with more than 1 word in the list
        {
            while(j<size-1)//due to the fact that i index the j+1th element
            {
                if(a[j].compareTo(newword)<0 && a[j+1].compareTo(newword)>0)
                   pos=j+1; //if its between two words, the (j+1)th position is the index
                else
                {
                    if(j+1==size-1 && pos==-1 && a[j+1].compareTo(newword)<0)//if the new word is bigger than the last element it will take the size as its index
                        pos=size;
                    else
                        if(j+1==size-1 && pos==-1 && a[0].compareTo(newword)>0)//if the new word is smaller than the last element it will take 0 as its index
                        {
                            pos=0;
                        }
                 }
                
             j++;   
            }
            if(capacity==size)//if word needs to be inserted and the list is full,allocate a bigger list
            {
                j=0;
                int capacity3=2*capacity;//doubles current capacity of list
                String []a= new String[capacity3];//creates a new array of strings equal to the new capacity
                while(k<capacity3)
                {
                    if(k==pos)//index of where new word should be added 
                    {
                        a[k]=newword;
                        k++;
                        continue;
                    }
                    if(j>=capacity)//if past the old capacity (before it was doubled),itll add null elements
                        a[k]=null;
                    else//otherwise itll take elements from the old list
                        a[k]=this.a[j];
                    
                    j++;//for indexing the old list
                    k++;//for going through the loop
                    
                }
                this.a=a; //list references newly created array
                this.size=size+1;//updates the size of the list 
                this.capacity=capacity3;//capacity of list is doubled
            }
            else//if the list isent full
            {
                if(a[0]!=null)//if the list isent empty
                {
                    j=0;
                    this.size+=1;//increases the size of list
                    String [] a=new String[capacity];
                    while(k<this.size)//loop to modify the old array
                    {
                        if(k==pos)//enters if at index of where new word should be inserted
                            a[k]=newword;
                        else//otherwise an element from the old list is taken 
                        {
                            a[k]=this.a[j];
                            j++;//old list index
                        }    
                        k++;    //loop increment
                    }
                    this.a=a;//new list references old one that was modified in the loop
                }

            }
            
            
        }
           
    }
    
    public void remove(String word)
    {
        int i=0,j=0,k=0,l=-1,pos=-1;
        while(i<size)//loop to detrmine if the word is in the list
        {
            if(a[i].compareTo(word)==0)
            {   l=0;//var used to determine if the word is in the list (0 if in list, -1 if not)
                pos=i;//index at where the word to be removed is
                break;
            }
            i++;
        }
        if(l>-1)//condition satisfied such that the word exists in the list
        {
            String []a=new String[capacity];//newly created array
            while(j<size)
            {
                if(j==pos)//skips element that is removed, effectively removing it 
                {
                    j++;
                    continue;
                }
                a[k]=this.a[j];//all old list element except for the removed element are put into new array
                k++;//loop counter
                j++;//for indexing old list
            }
          this.a=a;//old list references the modified array
          this.size-=1; //accounts for 1 less word in list
        }
        
        
    }
    public int find(String word)
    {
        int low=0,mid,high=size-1;
        while(high>=low)//condition for binary search
        {
            mid=(high+low)/2;
            if(a[mid].compareTo(word)==0)//searches middle element
                return mid;
            else
            {
                if(a[mid].compareTo(word)<0)//chops off lower half of the list
                    low=mid+1;    
                else//chops off upper half of the list
                    high=mid-1;          
            }
          
        }
        System.out.println("Key not found");//if no index is returned by the end of the loop, element is not found and -1 is returned
        return -1;
     
        
    }
    public WordList sublist(char init, char fin)
    {
        int j=0,i=0,k=0,list_size=0;
        while(j<size)//goes through all the words in the old list,finds all words between given characters (init and fin)
        {
            if(a[j].charAt(0)>=init && a[j].charAt(0)<=fin)//index 0 for first character comparaison, if the word is between start letter and end letter
                list_size++;//updates amount of words in new list
            j++;      
        }
        
        int capacity2= 2*list_size;//capacity of new wordlist object is 2 x the amount of words between given characters(init and fin)
        if(list_size==0)//if no words between given characters:init and fin, then the capacity is the same as the old list
        {
            capacity2=this.capacity;
        }
        
        WordList sub_list= new WordList(capacity2);//new wordlist object created with all null elements to begin with
        while(i<size)//going through the old list 
        {
            if(a[i].charAt(0)>=init && a[i].charAt(0)<=fin)
            {
                sub_list.a[k]=a[i];//adding all elements between given characters (init and fin) to new WordList object
                sub_list.size+=1;//updating the size of the list for the new WordList object
                k++;//new list index
            }
            i++;   //loop index
        }
        return sub_list;//returns new WordList object
    }
    
public String toString() {
        String longString = "";
	if(size==0)
	    longString = "The list is empty";
	else
	    longString = a[0];
        for (int i = 1; i < size; i++) {
            longString =longString + "\n" + a[i];
        }
        return longString;
    }
    
    /*public String toString()
    {
        String list="";
        int i=0;
        while(i<size)
        {
            list+=a[i];
            list+="\n";
            i++;
        }
        return list;
    }*/ //Just here incase i need it (my toString method)
}
