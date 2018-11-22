/*
Alexander Szebrag 
Lab Section 03
1148394
Lab 03

 */
package laab3;

public class DLLSet 
{
    private int size;
    private DLLNode head;
    private DLLNode tail;
    public DLLSet()//empty list
    {
        size=0;
        head=new DLLNode(0,null,null);
        tail=new DLLNode(0,null,head);
        head.next=tail;
    }
    
    public DLLSet(int[] sortedArray)
    {
        int i=0,dummy=0;
        DLLSet q=new DLLSet();
       // q.head=this.head;
        //q.tail=this.tail;
        while(i<sortedArray.length)
        {
            dummy=sortedArray[i];
            if(i==0)
            {
                DLLNode p=new DLLNode(dummy,q.tail,q.head);
                q.head.next=p;
                q.tail.prev=p;
                
                
                i++;
                size++;
                continue;
                
            }
           DLLNode p=new DLLNode(dummy,q.tail,q.tail.prev);
           q.tail.prev=p;
           p.prev.next=p;
           
           size++;
           i++;
            
        }
        this.head=q.head;
        this.tail=q.tail;
        
    }
    
    public int getSize()
    {
        return size;
    }
    
    public DLLSet copy()
    {
        if(tail.prev==head)
        {
            DLLSet dup= new DLLSet();
            return dup;
        }
        else
        {
            int i=0;
            DLLNode p= head.next;
            DLLSet dup= new DLLSet();
            while(p!=null&&i<size)
            {
                DLLNode q=new DLLNode(p.element,dup.tail,dup.tail.prev);
                q.prev.next=q;
                dup.tail.prev=q;
                dup.size++;
                p=p.next;
                i++;
            }
            return dup;
        }
           
    }
    
    public boolean isIn(int v)
    {
        DLLNode dummy1=head.next;
        DLLNode dummy2=tail;
        while(dummy1!=dummy2)
        {
            if(dummy1.element==v)
                return true;
            dummy1=dummy1.next;   
        }
        return false;
          
    }
    public void add(int v)
    {
        boolean truth;
        truth=this.isIn(v);
        if(truth==false)
        {
            if(head.next==tail)
            {
                DLLNode vnode=new DLLNode(v,tail,head);
                tail.prev=vnode;
                head.next=vnode;
                size++;    
            }
            DLLNode dummy= head.next;
            DLLNode dummy2=tail.prev;
            while(dummy!=tail)
            {
                if(v<head.next.element)//before first element
                {
                    DLLNode vnode=new DLLNode(v,head.next,head);
                    vnode.next.prev=vnode;
                    head.next=vnode;
                    size++;
                    break;
                    
                }
                if(v>dummy2.element)//after last element
                {
                    DLLNode vnode=new DLLNode(v,tail,tail.prev);
                    vnode.prev.next=vnode;
                    tail.prev=vnode;
                    size++;
                    break;
                }
                if(v>dummy.element && v<dummy.next.element)//add between 2 elements
                {
                    DLLNode vnode=new DLLNode(v,dummy.next,dummy);
                    dummy.next=vnode;
                    dummy=vnode;
                    size++;
                    break;
                    
                }
                
                dummy=dummy.next;
            }
            
            
        }
    }
    
    public void remove(int v)
    {
        boolean truth=this.isIn(v);
        if(truth==true)
        {
            DLLNode p = head.next;
            DLLNode q=tail.prev;
            while(p!=tail)
            {
                if(p.element==v)
                {
                    p.next.prev=p.prev;
                    p.prev.next=p.next;
                   
                    size--;
                    break;
                    
                }
             
                p=p.next;
            }
            
            
            
        }
        
    }
    
    public DLLSet union(DLLSet s)
    {
        DLLSet u= new DLLSet();
        DLLNode p=head.next;
        DLLNode q=s.head.next;
        
        if(p!=tail&&q!=s.tail)
        {
            while(p!=tail||q!=s.tail)
            {
                if(p==tail)
                {
                    u.addLast(q.element);
                    q=q.next;
                    continue;
                    
                }
                if(q==s.tail)
                {
                    u.addLast(p.element);
                    p=p.next;
                    continue;
                }
                if(p.element==q.element)
                {
                    u.addLast(q.element);
                    q=q.next;
                    p=p.next;
                    continue;
                    
                }
                if(p.element<q.element)
                {
                    u.addLast(p.element);
                    p=p.next;
                    continue;
                }
                if(p.element>q.element)
                {
                    u.addLast(q.element);
                    q=q.next;
                    continue;
                    
                }
                
                
            }
           return u;
            
        }
        else//union of one empty list and one non empty list
        {
            if(p==tail && q==s.tail)
                return new DLLSet();
                    
            if(p==tail)
                return s;
            if(q==s.tail)
                return this;
            
            
        }
        return u;
        
    }
    
    public DLLSet intersection(DLLSet s)
    {
         DLLSet u= new DLLSet();
        DLLNode p=head.next;
        DLLNode q=s.head.next;
        
        if(p!=tail&&q!=s.tail)
        {
            while(p!=tail||q!=s.tail)
            {
                if(p==tail)
                {
                   
                    q=q.next;
                    continue;
                    
                }
                if(q==s.tail)
                {
                    
                    p=p.next;
                    continue;
                }
                if(p.element==q.element)
                {
                    u.addLast(q.element);
                    q=q.next;
                    p=p.next;
                    continue;
                    
                }
                if(p.element<q.element)
                {
                    
                    p=p.next;
                    continue;
                }
                if(p.element>q.element)
                {
                    
                    q=q.next;
                    continue;
                    
                }
                
                
            }
           return u;
            
        }
        else//union of one empty list and one non empty list
        {
            if(p==tail && q==s.tail)
                return new DLLSet();
                    
            if(p==tail)
                return new DLLSet();
            if(q==s.tail)
                return new DLLSet();
            
            
        }
        return u;
        
        
        
    }
    
    
    public static DLLSet recUnion(DLLSet[] sArray)
    {
        return recUnion(sArray,0,sArray.length-1);
    }
    private static DLLSet recUnion(DLLSet[] sArray, int first,int last)
    {
        int temp,mid,left,right;//temp storage,middle of array,first element in the left array, first element in right array
        DLLSet []temp2=new DLLSet[500];
        DLLSet recUn=new DLLSet();//final set returned
        temp2=sArray;//temp to store copy of array
        if(first<last)
        {
            //split the array in half and sort each half
           mid=(first+last)/2;
           recUnion(temp2,first,mid);
          recUnion(temp2,mid+1,last); 
          
          //Merge the sorted arrays into one
          left=first;
          right=mid+1;
          //while there are numbers in the array to be sorted
          while(left<=mid&&right<=last)
          {
              //if the current number in the left array is larger than the current nummber in the right
              //array the numbers are moved around
              
              if(temp2[left].head.next.element>temp2[right].head.next.element)
              {
                  //the number that should be first is in the right array
                  temp=temp2[right].head.next.element;
                  //move the left array right one pos to make room for the smallerr number
                  for(int i=right-1;i>=left;i--)
                  {
                      temp2[i+1].head.next.element=temp2[i].head.next.element;
                  }
                  //put the smaller number where it belongs
                  temp2[left].head.next.element=temp;
                  //right array and mid are shifted right
                  right++;
                  mid++;
                  
                  
              }
              //no matter what the left array moves right
              left++;
          }
        }
        int k=0;
        
        while(k<temp2.length)
        {
            DLLNode d=temp2[k].head.next;
            recUn.addLast(d.element);
            k++;
            
            
        }
        return recUn;
        
    }
    
    public static DLLSet fastUnion(DLLSet[] sArray)
    {
        int first=0,last=sArray.length-1;
        DLLSet[] temp2=new DLLSet[last-first+1];
        DLLSet fastUn=new DLLSet();
        if(first<last)
        {
            int left=first;
            int mid=(first+last)/2;
            int right=mid+1;
            for(int i=0;i<temp2.length;i++)
            {
                if(left>mid)
                {
                    temp2[i]=sArray[right];
                    right++;
                }
                else
                    if(right>last)
                    {
                        temp2[i]=sArray[left];
                        left++;
                    }
                else
                        if(sArray[left].head.next.element<sArray[right].head.next.element)
                        {
                            temp2[i]=sArray[left];
                            left++;
                            
                        }
                    else
                        {
                            temp2[i]=sArray[right];
                            right++;
                        }
                
                        
                    
                
                
            }
            
         
            
            
        }
        
        int k=0;
        while(k<temp2.length)
        {
             DLLNode d=temp2[k].head.next;
            fastUn.addLast(d.element);
            k++;
            
        }
        return fastUn;
        
        
    }
    
    
    private void addLast(int v)
    {
        DLLNode p=new DLLNode(v,tail,tail.prev);
        tail.prev.next=p;
        tail.prev=p;
        size++;
        
    }
    public String toString() {
        String longString = "";
	if(size==0)
	    longString = "The set is empty";
        else{
            DLLNode p=head.next;
	    longString = new String("");
            for (; p.next!= tail ; p=p.next) {
                longString =longString +  p.element + "\n";          
            }//end for
            longString =longString +  p.element; 
        }
        return longString;
    }
    
    
    
}

 class DLLNode
{
    int element;
    DLLNode prev;
    DLLNode next;
    DLLNode(int i, DLLNode n, DLLNode p)
    {element=i;next=n;prev=p;}
    
}










