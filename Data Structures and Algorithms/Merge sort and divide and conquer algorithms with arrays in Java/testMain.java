package testing;

public class testMain {

	public static void main(String[] args) {
		int cap=6; //capacity
        int cap2=2; //capacity
        
        int i1=1; //valid position in words2
        int i2=4; //invalid position in words2 ( size<=i2<=capacity-1 )
        int i3=12; //invalid position in words2 ( i3<0 or i3>capacity-1 )
        
        //chosen according to the tests for sublist()
        char c1='i';
        char c2='k';
        char c3='h';
        char c4='m';
        char c5='b';
        char c6='h';  
        char c7='j'; 
        char c8='p'; 
        
        String[] words2={"add", "alpha", "boy", "car"}; //sorted, used to test insert & remove
	    String[] words3={"now", "then", "after", "five", "zoom"}; //unsorted, without repetitions - to test constructor 2
        String[] words4={"made","know","seven","know"};//unsorted with repetitions - to test constructor 2
        String[] words5={"fall", "flag","fly","ha", "haha", "ma", "me", "mm","my",  "so"};//to test sublist & find

	    String s2="buy";//word not in words2 - test insert inside list
        String s4="boy";//word in words2
        String s7="car";//last word of words2
	    String s6="mm";//word in words5 - test find()
	    String s1=s7+"ab";
        String s5=s1+"a";
	    String s8="aaabbb"; //smaller than first word in words 2
        
        // inputs end 
	//**************************************************************************************

 
        //test constructor 1
        WordList listObj1= new WordList(cap);
        System.out.println("Test 1 - Constructor 1:\n"+"List:\n"+ listObj1.toString());
        System.out.println("capacity="+listObj1.getCapacity());
        System.out.println("size="+listObj1.getSize());        
        
        
        System.out.println("*************************************************************");
        //test constructor 2 with sorted input without repetitions
       
        WordList listObj2= new WordList(words2);
        //test if words are stored correctly
        System.out.println("Test 2 - Constructor 2 (sorted input):\n"+"List:\n"+listObj2.toString());
        System.out.println("capacity="+listObj2.getCapacity());
        System.out.println("size="+listObj2.getSize());

	
	System.out.println("*************************************************************");
        //test constructor 2 - unsorted input without duplicates
        
        WordList listObj4= new WordList(words3);
        //display listObj4
        System.out.println("Test 3 - Constructor 2 (unsorted input without repetitions):\n"+"List:\n"+listObj4.toString());
        System.out.println("capacity="+listObj4.getCapacity());
        System.out.println("size="+listObj4.getSize());

 
	System.out.println("*************************************************************");
        //test constructor 2 - unsorted input & with duplicates
        listObj4= new WordList(words4);
        //display listObj4
        System.out.println("Test 4 - Constructor 2 (unsorted input with repetitions):\n"+"List:\n"+listObj4.toString());
        System.out.println("capacity="+listObj4.getCapacity());
        System.out.println("size="+listObj4.getSize());
              
        
        System.out.println("*************************************************************");
        // test insert one word to listObj2 at the end
        listObj2.insert(s1);
        System.out.println("Test 5 - insert at end of list, newword: "+s1+"\nList:\n"+listObj2.toString());
        System.out.println("capacity="+listObj2.getCapacity());
        System.out.println("size="+listObj2.getSize());
                
             
        System.out.println("*************************************************************");
        //test insert inside list 
        listObj2=new WordList(words2);
        listObj2.insert(s2);
        System.out.println("Test 6 - insert inside list, newword: "+s2+"\nList:\n"+listObj2.toString());
        System.out.println("capacity="+listObj2.getCapacity());
        System.out.println("size="+listObj2.getSize());


	System.out.println("*************************************************************");
        //test insert at front 
        listObj2=new WordList(words2);
        listObj2.insert(s8);
        System.out.println("Test 7 - insert at front, newword: "+s8+"\nList:\n"+listObj2.toString());
        System.out.println("capacity="+listObj2.getCapacity());
        System.out.println("size="+listObj2.getSize());
        

         System.out.println("*************************************************************");
        //attempt to insert when word is in list
        listObj2=new WordList(words2);
        listObj2.insert(s4);
        System.out.println("Test 8 - attempt to insert when word is in list, newword: "+s4+"\nList:\n"+listObj2.toString());
        System.out.println("capacity="+listObj2.getCapacity());
        System.out.println("size="+listObj2.getSize());
        

         System.out.println("*************************************************************");
        //test insert in empty list
        listObj1= new WordList(cap);
        listObj1.insert(s1);
        System.out.println("Test 9 - insert "+s1+ " in empty list:\n"+"List:\n"+listObj1.toString());
        System.out.println("capacity="+listObj1.getCapacity());
        System.out.println("size="+listObj1.getSize());
        
        
        System.out.println("*************************************************************");
        //test insert when size==capacity and neword not in list 
        listObj2= new WordList(cap2);
        for(int i=0;i<cap2;i++){
            listObj2.insert(s1);
            s1=s1+"a";
        }
        System.out.println("Test 10 - insert - size==capacity, new word not in list, newword: "+s2);
        listObj2.insert(s2);
        System.out.println("List:\n"+listObj2.toString());
        System.out.println("capacity="+listObj2.getCapacity());
        System.out.println("size="+listObj2.getSize());             
        
        
         System.out.println("*************************************************************");
        //test getWordAt valid position
        listObj2=new WordList(words2);
        try{
            System.out.println("Test 11 - getWordAt(i) - valid index i");
            System.out.println(listObj2.getWordAt(i1));
        }
        catch(ArrayIndexOutOfBoundsException e){System.out.println(e);}

        
        System.out.println("*************************************************************");
        //test getWordAt invalid list position
        try{
            System.out.println("Test 12 - getWordAt(i) - invalid index i");
            System.out.println(listObj2.getWordAt(i2));
        }
        catch(ArrayIndexOutOfBoundsException e){System.out.println(e);}


	System.out.println("*************************************************************");
        //test getWordAt invalid list position
        try{
            System.out.println("Test 13 - getWordAt(i) - invalid index i");
            System.out.println(listObj2.getWordAt(i3));
        }
        catch(ArrayIndexOutOfBoundsException e){System.out.println(e);}
        
        
        System.out.println("*************************************************************");
        //test binary search:
        listObj2= new WordList(words5);
        System.out.println("Test 14 - find - key not in list, key is " + s2);
        int searchIndex=listObj2.find(s2);
        System.out.println("returned index: "+ searchIndex);


        System.out.println("*************************************************************");
        System.out.println("Test 15 - find - key  in list, key is " + s6);
        searchIndex=listObj2.find(s6);
        System.out.println("returned index: "+ searchIndex);
        

         System.out.println("*************************************************************");
        //test remove
        System.out.println("Test 16 - remove - word not in list, word is "+s2);
        listObj2=new WordList(words2);
        listObj2.remove(s2);
        System.out.println("List: \n"+listObj2.toString());
        System.out.println("capacity="+listObj2.getCapacity());
        System.out.println("size="+listObj2.getSize());


         System.out.println("*************************************************************");
        //test remove from inside or beginning
        listObj2= new WordList(words2);
        System.out.println("Test 17 - remove from inside or beginning, word is "+s4);
        listObj2.remove(s4);
        System.out.println("List: \n"+listObj2.toString());
        System.out.println("capacity="+listObj2.getCapacity());
        System.out.println("size="+listObj2.getSize());


        System.out.println("*************************************************************");
        //test remove from empty list
        System.out.println("Test 18 - remove from empty list");
        WordList listObj5= new WordList(cap);
        listObj5.remove(s7);
        System.out.println("List: \n"+listObj5.toString());
        System.out.println("capacity="+listObj5.getCapacity());
        System.out.println("size="+listObj5.getSize());

        
        System.out.println("*************************************************************");
        //test sublist  - from empty list - its capacity could be any positive value
        System.out.println("Test 19 - sublist from empty list ");
        WordList listObj6= new WordList(cap);
        WordList listObj7=listObj6.sublist(c3,c4);
        System.out.println("sublist: \n"+listObj7.toString());
        System.out.println("capacity="+listObj7.getCapacity());
        System.out.println("size="+listObj7.getSize());
        
        
        System.out.println("*************************************************************");
        //test sublist  - empty sublist from non empty list - its capacity could be any positive value
        System.out.println("Test 20 - empty sublist from non empty list ");
        listObj6= new WordList(words5);
        listObj7=listObj6.sublist(c1,c2);
        System.out.println("sublist: \n"+listObj7.toString());
        System.out.println("capacity="+listObj7.getCapacity());
        System.out.println("size="+listObj7.getSize());
               
        
        System.out.println("*************************************************************");
        //test sublist - non-empty sublist; words starting with init and fin are in list (more than one for each)
        System.out.println("Test 21 - non-empty sublist ");
        listObj6= new WordList(words5);
        listObj7=listObj6.sublist(c3,c4);
        System.out.println("sublist: \n"+listObj7.toString());
        System.out.println("capacity="+listObj7.getCapacity());
        System.out.println("size="+listObj7.getSize());
        //System.out.println("Initial list: \n"+listObj6.toString());


	System.out.println("*************************************************************");
        //test sublist - non-empty sublist words starting with init and fin are not in list
        System.out.println("Test 22 - non-empty sublist ");
        listObj6= new WordList(words5);
        listObj7=listObj6.sublist(c7,c8);
        System.out.println("sublist: \n"+listObj7.toString());
        System.out.println("capacity="+listObj7.getCapacity());
        System.out.println("size="+listObj7.getSize());
               
        
        
        System.out.println("*************************************************************");
        //test sublist  - sublist is a prefix or suffix
        System.out.println("Test 23 - sublist is a prefix or a suffix");
        listObj6= new WordList(words5);
        listObj7=listObj6.sublist(c5,c6);
        System.out.println("sublist: \n"+listObj7.toString());
        System.out.println("capacity="+listObj7.getCapacity());
        System.out.println("size="+listObj7.getSize());
		

	}

}
