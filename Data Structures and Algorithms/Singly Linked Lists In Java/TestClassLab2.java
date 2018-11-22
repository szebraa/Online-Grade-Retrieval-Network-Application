public class TestWordLinkedList {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        int cap=6; //capacity
        int cap2=2; //capacity
        
        int i1=1; //valid position in words2
      
        int i3=12; //invalid position in words2 ( i3<0 or i3>size-1 )
        
                
        String[] words2={"add", "alpha", "boy", "car"}; //sorted, used to test insert, remove, find
	String[] words3={"now", "then", "after", "five", "zoom"}; //unsorted, without repetitions - to test constructor 2
        String[] words4={"made","know","seven","know"};//unsorted with repetitions - to test constructor 2
        String[] words6={"eta","gamma", "zeta"};//to test mergeTo
        String[] words7={"alpha","beta","phi"};//to test mergeTo - no common words with words6
        String[] words8={"alpha","gamma","zeta"};;//to test mergeTo - has common words with words6

	String s2="buy";//word not in words2 - test insert inside list
        String s4="boy";//word in words2
        String s7="car";//last word of words2
	String s1=s7+"ab";
        String s5=s1+"a";
	String s8="aaabbb"; //smaller than first word in words 2
        
        // inputs end 
	//**************************************************************************************

 
        //test constructor 1
        WordLinkedList listObj1= new WordLinkedList();
        System.out.println("Test 1 - Constructor 1:\n"+"List:\n"+ listObj1.toString());
        System.out.println("size="+listObj1.getSize());        
        
        
        System.out.println("*************************************************************");
        //test constructor 2 with sorted input without repetitions
       
        WordLinkedList listObj2= new WordLinkedList(words2);
        //test if words are stored correctly
        System.out.println("Test 2 - Constructor 2 (sorted input):\n"+"List:\n"+listObj2.toString());
        System.out.println("size="+listObj2.getSize());

	
	System.out.println("*************************************************************");
        //test constructor 2 - unsorted input without duplicates
        
        WordLinkedList listObj4= new WordLinkedList(words3);
        //display listObj4
        System.out.println("Test 3 - Constructor 2 (unsorted input without repetitions):\n"+"List:\n"+listObj4.toString());
        System.out.println("size="+listObj4.getSize());

 
	System.out.println("*************************************************************");
        //test constructor 2 - unsorted input & with duplicates
        
        listObj4= new WordLinkedList(words4);
        //display listObj4
        System.out.println("Test 4 - Constructor 2 (unsorted input with repetitions):\n"+"List:\n"+listObj4.toString());
        System.out.println("size="+listObj4.getSize());
              
        
        System.out.println("*************************************************************");
        // test insert one word to listObj2 at the end
        listObj2.insert(s1);
        System.out.println("Test 5 - insert at end of list, newword: "+s1+"\nList:\n"+listObj2.toString());
        System.out.println("size="+listObj2.getSize());
                
             
        System.out.println("*************************************************************");
        //test insert inside list 
        listObj2=new WordLinkedList(words2);
        listObj2.insert(s2);
        System.out.println("Test 6 - insert inside list, newword: "+s2+"\nList:\n"+listObj2.toString());
        System.out.println("size="+listObj2.getSize());


	System.out.println("*************************************************************");
        //test insert at front 
        listObj2=new WordLinkedList(words2);
        listObj2.insert(s8);
        System.out.println("Test 7 - insert at front, newword: "+s8+"\nList:\n"+listObj2.toString());
        System.out.println("size="+listObj2.getSize());
        

         System.out.println("*************************************************************");
        //attempt to insert when word is in list
        listObj2=new WordLinkedList(words2);
        listObj2.insert(s4);
        System.out.println("Test 8 - attempt to insert when word is in list, newword: "+s4+"\nList:\n"+listObj2.toString());
        System.out.println("size="+listObj2.getSize());
        

         System.out.println("*************************************************************");
        //test insert in empty list
        listObj1= new WordLinkedList();
        listObj1.insert(s1);
        System.out.println("Test 9 - insert "+s1+ " in empty list:\n"+"List:\n"+listObj1.toString());
        System.out.println("size="+listObj1.getSize());
        
                   
        
        
         System.out.println("*************************************************************");
        //test getWordAt valid position
        listObj2=new WordLinkedList(words2);
        try{
            System.out.println("Test 10 - getWordAt(i) - valid index i");
            System.out.println(listObj2.getWordAt(i1));
        }
        catch(IndexOutOfBoundsException e){System.out.println(e);}

        
      
	System.out.println("*************************************************************");
        //test getWordAt invalid list position
        try{
            System.out.println("Test 11 - getWordAt(i) - invalid index i");
            System.out.println(listObj2.getWordAt(i3));
        }
        catch(IndexOutOfBoundsException e){System.out.println(e);}
        
         
         System.out.println("*************************************************************");
        //test remove - valid position inside list
        listObj2=new WordLinkedList(words2);
        try{
            System.out.println("Test 11 - remove(i) - valid index i");
            System.out.println("Word removed: " + listObj2.remove(i1));
            System.out.println("List: \n"+listObj2.toString());
            System.out.println("size="+listObj2.getSize());
        }
        catch(IndexOutOfBoundsException e){System.out.println(e);}
        
       System.out.println("*************************************************************");
        //test remove first
        listObj2=new WordLinkedList(words2);
        try{
            System.out.println("Test 12 - remove(0)");
            System.out.println("Word removed: " + listObj2.remove(0));
            System.out.println("List: \n"+listObj2.toString());
            System.out.println("size="+listObj2.getSize());
        }
        catch(IndexOutOfBoundsException e){System.out.println(e);}
        
        System.out.println("*************************************************************");
        //test remove last
        listObj2=new WordLinkedList(words2);
        try{
            System.out.println("Test 13 - remove last");
            System.out.println("Word removed: " + listObj2.remove(listObj2.getSize()-1));
            System.out.println("List: \n"+listObj2.toString());
            System.out.println("size="+listObj2.getSize());
        }
        catch(IndexOutOfBoundsException e){System.out.println(e);}
        
	System.out.println("*************************************************************");
        //test remove - invalid position
        try{
            System.out.println("Test 14 - remove(i) - invalid index i");
            listObj2.remove(i3);
            System.out.println("List: \n"+listObj2.toString());
            System.out.println("size="+listObj2.getSize());
        }
        catch(IndexOutOfBoundsException e){System.out.println(e);}
        
        
        System.out.println("*************************************************************");
        //test find
        listObj2= new WordLinkedList(words2);
        System.out.println("Test 15 - find - key not in list, key is " + s2);
        int searchIndex=listObj2.find(s2);
        System.out.println("returned index: "+ searchIndex);


        System.out.println("*************************************************************");
        System.out.println("Test 16 - find - key  in list, key is " + s4);
        listObj2= new WordLinkedList(words2);
        searchIndex=listObj2.find(s4);
        System.out.println("returned index: "+ searchIndex);
        

        System.out.println("*************************************************************");
        //test mergeTo, no words in common
        System.out.println("Test 17 - mergeTo");
        listObj1=new WordLinkedList(words6);
        listObj2=new WordLinkedList(words7);
        listObj1.mergeTo(listObj2);
        System.out.println("this list: \n"+listObj1.toString());
        System.out.println("size of this list = " + listObj1.getSize());
        System.out.println("that list: \n"+listObj2.toString());
        System.out.println("size of that list = " + listObj2.getSize());
        
        
        System.out.println("*************************************************************");
        //test mergeTo, no words in common
        System.out.println("Test 18 - mergeTo");
        listObj1=new WordLinkedList(words7);
        listObj2=new WordLinkedList(words6);
        listObj1.mergeTo(listObj2);
        System.out.println("this list: \n"+listObj1.toString());
        System.out.println("size of this list = " + listObj1.getSize());
        System.out.println("that list: \n"+listObj2.toString());
        System.out.println("size of that list = " + listObj2.getSize());
        
        
         System.out.println("*************************************************************");
        //test mergeTo, one word in common
        System.out.println("Test 19 - mergeTo");
        listObj1=new WordLinkedList(words8);
        listObj2=new WordLinkedList(words6);
        listObj1.mergeTo(listObj2);
        System.out.println("this list: \n"+listObj1.toString());
        System.out.println("size of this list = " + listObj1.getSize());
        System.out.println("that list: \n"+listObj2.toString());
        System.out.println("size of that list = " + listObj2.getSize());
        
         System.out.println("*************************************************************");
        //test mergeTo, this list empty
        System.out.println("Test 20 - mergeTo");
        listObj1=new WordLinkedList();
        listObj2=new WordLinkedList(words7);
        listObj1.mergeTo(listObj2);
        System.out.println("this list: \n"+listObj1.toString());
        System.out.println("size of this list = " + listObj1.getSize());
        System.out.println("that list: \n"+listObj2.toString());
        System.out.println("size of that list = " + listObj2.getSize());
        
        
         System.out.println("*************************************************************");
        //test mergeTo that list empty
        System.out.println("Test 21 - mergeTo");
        listObj1=new WordLinkedList(words6);
        listObj2=new WordLinkedList();
        listObj1.mergeTo(listObj2);
        System.out.println("this list: \n"+listObj1.toString());
        System.out.println("size of this list = " + listObj1.getSize());
        System.out.println("that list: \n"+listObj2.toString());
        System.out.println("size of that list = " + listObj2.getSize());
 
        
    }
}
