public class TestDLLSet {

       public static void main(String[] args) {
        
        
        int m= 16; //size of array of sets
        int[] set2={ -9, -4, 0, 6}; //sorted
	int[] set6={-20, 4, 9, 77};//to test union, intersection
        int[] set7={-10, 1, 3};//to test union, intersection - no common elements with set6
        int[] set8={-20, 5, 9, 12};//to test union, intersection - has common elements with set6
       
        int s1 = 20; // larger than any value in set2
        int s2 = 2; // test add "inside" set2, value not in set 2, in between smallest and largest of set2
        int s8 = -100; // smaller than any value in set2
        int s4 = -4; //value in set2
        int s3 = -9; //smallest element of set2
        int s5 = 6; //largest element of set2
        // inputs end 
	//**************************************************************************************
        
        //test constructor 1 
        DLLSet setObj1= new DLLSet();
        System.out.println("Test 1 - Constructor 1:\n"+"Set:\n"+ setObj1.toString());
        System.out.println("size="+setObj1.getSize());        
        
        
        System.out.println("*************************************************************");
        //test constructor 2        
        DLLSet setObj2= new DLLSet(set2);
        System.out.println("Test 2 - Constructor 2:\n"+"Set:\n"+setObj2.toString());
        System.out.println("size="+setObj2.getSize());
	           
        System.out.println("*************************************************************");
        //test isIn
        setObj2= new DLLSet(set2);
        System.out.println("Test 3 - isIn - value not in set, value is " + s2);
        System.out.println(setObj2.isIn(s2));


        System.out.println("*************************************************************");
        System.out.println("Test 4 - isIn - value  in set, value is " + s4);
        setObj2= new DLLSet(set2);
        System.out.println(setObj2.isIn(s4));
        
        System.out.println("*************************************************************");
        // test add one element to setObj2 at the end
        setObj2.add(s1);
        System.out.println("Test 5 - add at end of list, value: "+s1+"\nSet:\n"+setObj2.toString());
        System.out.println("size="+setObj2.getSize());
                
             
        System.out.println("*************************************************************");
        //test add inside 
        setObj2=new DLLSet(set2);
        setObj2.add(s2);
        System.out.println("Test 6 - add inside list, value: "+s2+"\nSet:\n"+setObj2.toString());
        System.out.println("size="+setObj2.getSize());


	System.out.println("*************************************************************");
        //test add at front 
        setObj2=new DLLSet(set2);
        setObj2.add(s8);
        System.out.println("Test 7 - add at front, value: "+s8+"\nSet:\n"+setObj2.toString());
        System.out.println("size="+setObj2.getSize());
        

         System.out.println("*************************************************************");
        //attempt to add when value is in set
        setObj2=new DLLSet(set2);
        setObj2.add(s4);
        System.out.println("Test 8 - attempt to add when value is in set, value: "+s4+"\nSet:\n"+setObj2.toString());
        System.out.println("size="+setObj2.getSize());
        

         System.out.println("*************************************************************");
        //test add in empty set
        setObj1= new DLLSet();
        setObj1.add(s1);
        System.out.println("Test 9 - add "+s1+ " in empty set:\n"+"Set:\n"+setObj1.toString());
        System.out.println("size="+setObj1.getSize());     
           
        System.out.println("*************************************************************");
        //test copy
        setObj1= new DLLSet(set2);
        setObj2=setObj1.copy();
        System.out.println("Test 10 - copy:\n"+"Copy:\n"+setObj2.toString());
        System.out.println("size="+setObj2.getSize()); 
        setObj2.add(s2);
        System.out.println("Change in copy should not affect the initial set:\nInitial set:\n"+setObj1.toString()); 
        
        System.out.println("*************************************************************");
        //test remove - value in set
        setObj2=new DLLSet(set2);
            System.out.println("Test 11 - remove value from set");
            setObj2.remove(s4);
            System.out.println("Set: \n"+setObj2.toString());
            System.out.println("size="+setObj2.getSize());
       
       System.out.println("*************************************************************");
        //test remove first
        setObj2=new DLLSet(set2);
            System.out.println("Test 12 - remove first");
          setObj2.remove(s3);
            System.out.println("Set: \n"+setObj2.toString());
            System.out.println("size="+setObj2.getSize());
        
            
        System.out.println("*************************************************************");
        //test remove last
        setObj2=new DLLSet(set2);
            System.out.println("Test 13 - remove last");
            setObj2.remove(s5);
            System.out.println("Set: \n"+setObj2.toString());
            System.out.println("size="+setObj2.getSize());
        
            
	System.out.println("*************************************************************");
        //test remove - value not in set
         setObj2=new DLLSet(set2);
           System.out.println("Test 14 - remove - value not in set");
           setObj2.remove(s2);
            System.out.println("Set: \n"+setObj2.toString());
            System.out.println("size="+setObj2.getSize());
            
        
         System.out.println("*************************************************************");
        //test remove from empty set
        setObj1= new DLLSet();
        setObj1.remove(s2);
        System.out.println("Test 15 - remove from empty set:\n"+"Set:\n"+setObj1.toString());
        System.out.println("size="+setObj1.getSize());
        

        System.out.println("*************************************************************");
        //test union, no element in common
        System.out.println("Test 16 - union");
        setObj1=new DLLSet(set6);
        setObj2=new DLLSet(set7);
        DLLSet setObj3=setObj1.union(setObj2);
        System.out.println("union: \n"+setObj3.toString());
        System.out.println("size of union = " + setObj3.getSize()); 
        System.out.println("this set: \n"+setObj1.toString());
        System.out.println("set s: \n"+setObj2.toString());
               
        
        System.out.println("*************************************************************");
        //test union, no element in common
        System.out.println("Test 17 - union");
        setObj1=new DLLSet(set7);
        setObj2=new DLLSet(set6);
        setObj3=setObj1.union(setObj2);
        System.out.println("union: \n"+setObj3.toString());
        System.out.println("size of union = " + setObj3.getSize());
        
        
         System.out.println("*************************************************************");
        //test union, elements in common
        System.out.println("Test 18 - union");
        setObj1=new DLLSet(set8);
        setObj2=new DLLSet(set6);
        setObj3=setObj1.union(setObj2);
        System.out.println("union: \n"+setObj3.toString());
        System.out.println("size of union = " + setObj3.getSize());
        
        System.out.println("*************************************************************");
        //test union, this set empty
        System.out.println("Test 19 - union with empty set");
        setObj1=new DLLSet();
        setObj2=new DLLSet(set7);
        setObj3=setObj1.union(setObj2);
        System.out.println("union: \n"+setObj3.toString());
        System.out.println("size of union = " + setObj3.getSize());
        
        
        System.out.println("*************************************************************");
        //test union that set empty
        System.out.println("Test 20 - union with empty set");
        setObj1=new DLLSet(set6);
        setObj2=new DLLSet();
        setObj3=setObj1.union(setObj2);
        System.out.println("union: \n"+setObj3.toString());
        System.out.println("size of union = " + setObj3.getSize());
        
        
         System.out.println("*************************************************************");
        //test intersection, no element in common
        System.out.println("Test 21 - intersection");
        setObj1=new DLLSet(set6);
        setObj2=new DLLSet(set7);
        setObj3=setObj1.intersection(setObj2);
        System.out.println("intersection: \n"+setObj3.toString());
        System.out.println("size of intersection = " + setObj3.getSize());
        System.out.println("this set: \n"+setObj1.toString());
        System.out.println("set s: \n"+setObj2.toString());
               
        
        System.out.println("*************************************************************");
        //test intersection, elements in common
        System.out.println("Test 22 - intersection");
        setObj1=new DLLSet(set6);
        setObj2=new DLLSet(set8);
        setObj3=setObj1.intersection(setObj2);
        System.out.println("intersection: \n"+setObj3.toString());
        System.out.println("size of intersection = " + setObj3.getSize());
        
        
         System.out.println("*************************************************************");
        //test intersection, elements in common
        System.out.println("Test 23 - intersection");
        setObj1=new DLLSet(set8);
        setObj2=new DLLSet(set6);
        setObj3=setObj1.intersection(setObj2);
        System.out.println("intersection: \n"+setObj3.toString());
        System.out.println("size of intersection = " + setObj3.getSize());
        
        System.out.println("*************************************************************");
        //test intersection, this set empty
        System.out.println("Test 24 - intersection with empty set");
        setObj1=new DLLSet();
        setObj2=new DLLSet(set7);
        setObj3=setObj1.intersection(setObj2);
        System.out.println("intersection: \n"+setObj3.toString());
        System.out.println("size of intersection = " + setObj3.getSize());
        
        
        System.out.println("*************************************************************");
        //test intersection, that set empty
        System.out.println("Test 25 - intersection with empty set");
        setObj1=new DLLSet(set6);
        setObj2=new DLLSet();
        setObj3=setObj1.intersection(setObj2);
        System.out.println("intersection: \n"+setObj3.toString());
        System.out.println("size of intersection = " + setObj3.getSize());
        
         System.out.println("*************************************************************");
        //test recursive union
         System.out.println("Test 26 - recursive union");
         DLLSet[] sets = new DLLSet[m];
         for(int i=0; i<m; i++){
             sets[i] = new DLLSet();
             sets[i].add(i);
         }
        setObj3 = DLLSet.recUnion(sets);
        System.out.println("union: \n"+setObj3.toString());
        System.out.println("size of union = " + setObj3.getSize());
        
         System.out.println("*************************************************************");
        //test non-recursive union
         System.out.println("Test 27 - non-recursive union");
        sets = new DLLSet[m];
         for(int i=0; i<m; i++){
             sets[i] = new DLLSet();
             sets[i].add(i);
         }
        setObj3 = DLLSet.fastUnion(sets);
        System.out.println("union: \n"+setObj3.toString());
        System.out.println("size of union = " + setObj3.getSize());
    }
}
