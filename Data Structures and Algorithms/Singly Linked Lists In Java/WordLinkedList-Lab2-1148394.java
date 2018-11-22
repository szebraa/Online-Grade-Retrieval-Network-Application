/*
Alexander Szebrag 
Lab Section 03
1148394
Lab 02

 */
package laab2;

/**
 *
 * @author Dmytro
 */
public class WordLinkedList 
{
    private Node<String> head;
    private int size;
    public WordLinkedList()
    {
        head= new Node<String>(null,null);
        Node<String> q=new Node<String>(null,null);
        head.next=q;
        size=0;
    }
    public WordLinkedList(String[] arrayOfWords)
    {
          int len=arrayOfWords.length,i=0,j=0;
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
        
        //SECOND PORTION: deals with creating the list and adding the elements
        this.size=len;//makes size of list equal to the effective length found by going through the 2 loops (used to elimimate 2 identicle elements)
        
        head= new Node<String>(null,null);//creation of head
        
        if(arrayOfWords[0]!=null)//add first element to linked list
        {
            Node <String> p=new Node<String>(arrayOfWords[0],null);//new node created to point at null (last element)
            head.next=p;//head points at newly created node
            p=p.next;
            
        }
        else
        {
           Node <String> p=new Node<String>(null,null);//node that points at null
            size=0;//no elements in list
        }
        
        Node <String> p=new Node<String>(arrayOfWords[0],null);//kept incase
        head.next=p;//kept incase
        
        
        i=1;//starts at second element of array
        while(i<this.size)
        {
           Node <String> q=new Node<String>(arrayOfWords[i],p.next);//new nodes created
            p.next=q;//first time through, element after dummy head references new node
            p=p.next;//go trough to the last created node
            q=q.next;//go along through the linked list
            i++;
        }
        Node <String> q=new Node<String>(null,p.next);//end of list  
    }
        
    public int getSize()
    {
        return size;
    }
    public String getWordAt(int i)
    {
        if(i>=0&&i<size-1)//check for proper index passed
        { 
            Node <String> p=head.next;
            int j=0;
            while(j<size&&p!=null)
            {
                if(j==i)//if element found at index
                {
                    return p.element;
                }
                p=p.next;
                j++;
                
            }   
        }
            
        else//if not exception is thrown
             throw new ArrayIndexOutOfBoundsException("This index is not valid!");
             return "This index is not valid!";//wouldnt work without returning this
           
    }
    public void insert(String newword)
    {
        
        Node <String> p=head.next;//node element referencing the first actual element on the node (not dummy)
        while (p!=null)//goes through list until it finds the position to be inserted (until end)
        {
            if(newword==null)//no word to be inserted
                break;
            
            if(head.next.element==null)//for empty lists
            {
                Node <String> q= new Node<String>(newword,null);//creation of new node linked to the end(null)
                head.next=q;//links the beginning of the list(from the dummy node) to the newly created node (last element) 
                size++;
                break;
            }
            if(newword.compareTo(p.element)==0)//nothing is done if it is already in the list
                break;
              
            else
            {
                if(p.next!=null&& newword.compareTo(p.element)>0 && newword.compareTo(p.next.element)<0)//situation where insertion is between two words
                {
                    Node <String> q= new Node<String>(newword,p.next);//new node created pointing to the next element of the current list
                    p.next=q;//makes current element of the list point at new created element (the position before the new word is inserted)
                    size++;
                    break;
                }
                else
                {
                    if(p.next==null&& newword.compareTo(p.element)>0)//insertion at end of the list
                    {
                        Node <String> q= new Node<String>(newword,p.next);//creation of new node pointing at null (last element)
                        p.next=q;//element before null points at the new last element
                        size++;
                        break;
                
                    }
                    else
                    {
                        if(p.next==null&& newword.compareTo(head.next.element)<0)//insertion at the beginning of the list
                        {
                            Node <String> q= new Node<String>(newword,head.next);//new node pointing at element after dummy node
                            head.next=q;//dummy node pointing at the newly created node
                            size++;
                            break;
                        }
                    }
                }
                
            }
            p=p.next; //to go through the linked list    
        }    
    }
    public int find(String word)
    {
        int pos=0;
        Node <String> p= head.next;
        while(p!=null)
        {
            if(p.element.compareTo(word)==0)
                return pos;
            
            pos++;
            p=p.next;
            
        }
        return -1;
    }
    public String remove(int i)
    {
        
        if(i>=0 && i<size)
        {
            int pos=0;
            String temp;
            Node <String>p=head;
            while(p!=null)
            {
                if(pos==i)//when the removed index is found
                {
                    temp=p.next.element;//stores element to be removed in temp variable
                    p.next=p.next.next;//previous element before the removed element now points at element after the removed element
                    size--;
                    return temp;//returns removed element
                    
                }
                pos++;
                p=p.next;
            }
            
            
        }
        else
            throw new ArrayIndexOutOfBoundsException("This index is not valid!");
            
       return "This index is not valid!";   
    }
    
    public void mergeTo(WordLinkedList that)
    {
        
        while(that.head.next!=null)//the inefficient solution (MAY BE ABLE TO EDIT TO MAKE MORE EFFICIENT)-tried for way too long gave up...    
        {
            //but really its not that inefficient, it runs at big theta(Cn1 +n2), where C is a const
            this.insert(that.head.next.element);//searches through this linked list, puts in word from that linked list
            that.head.next=that.head.next.next;//moves on to the next element of that linked list
            if(that.size>0)//decrements until the size of that list is empty
            that.size--;
        }
    }
    
    public String toString() 
{
        String longString = "";
	if(size==0)
	    longString = "The list is empty";
        else{
            Node p=head.next;
	    longString = new String("");
            for (; p.next!= null ; p=p.next) {
                longString =longString +  p.element+ "\n";          
            }//end for
            longString =longString +  p.element; 
        }
        return longString;
}
    
}

class Node<String>
{
    String element;
    Node<String> next;
    public Node(String e, Node<String> n)
    {
        element=e;
        next=n;
    }
   
}
