Class Test inherits IO {

    (* Defining a method to check if a number is even *)
    isEven(n: Int): Bool {
        if (n / 2) * 2 = n then
            true
        else
            false
        fi
    };
  
  	(* Method to test various operators on an integer *)
    manyTests(n: Int): Int {
        {
            let result: Int <- n in
            {
              	result <- ~ result;
                result <- result + 10; 
                result <- result - 5;  
                result <- result * 2;  
                result <- result / 3;  
              	if result <= 0 then
            		0
        		else
            		result + 10
        		fi;
            };
        }
    };
	
  	(* Method to demonstrate more complex features *)
    complexTests(): Object {
        {
            let str: String <- "Hello, world!" in
            {
                out_string("Original string: "); out_string(str); out_string("\n");

                (* String concatenation *)
                let newStr: String <- str.concat(" More test string stuff") in
                {
                    out_string("Concatenated string: "); out_string(newStr); out_string("\n");
                };

                (* Substring extraction *)
                let subStr: String <- str.substr(7, 5) in
                {
                    out_string("Substring from index 7 to 11: "); out_string(subStr); out_string("\n");
                };

                (* String length *)
                let length: Int <- str.length() in
                {
                    out_string("Length of the string: "); out_int(length); out_string("\n");
                };

                (* Polymorphic dispatch example *)
                let testObj: Test <- self in
                {
                    out_string("Polymorphic dispatch example: "); testObj.manyTests(5); out_string("success\n");
                };
            };
        }
    };
  
    (* Defining a method to calculate the factorial of a number *)
    factorial(n: Int): Int {
        if n <= 1 then
            1
        else
            n * factorial(n - 1)
        fi
    };    
};

Class Main inherits IO {
  
  	(* Method to test dynamic dispatch *)
    testDynamicDispatch(ioObj: IO): Object {
        {
            out_string("Testing dynamic dispatch: ");
            ioObj.out_string("This is dynamically dispatched\n");
        }
    };
    
    main(): Object {
        {
            let testObj: Test <- new Test in
            let num : Int <- 10 in
            {
                out_string("Testing if "); out_int(num); out_string(" is even: ");
                if testObj.isEven(num) then
                    out_string("Yes\n")
                else
                    out_string("No\n")
                fi;

                out_string("Factorial of "); out_int(num); out_string(" is: ");
                out_int(testObj.factorial(num)); out_string("\n");
              	out_string("Random tests of "); out_int(num); out_string(" is: ");
              	out_int(testObj.manyTests(num)); out_string("\n");
              	testObj.complexTests();
              	(* Call the dynamic dispatch method with an instance of Test *)
                testDynamicDispatch(testObj);

                (* Call the dynamic dispatch method with an instance of IO *)
                testDynamicDispatch(self);
            };
        }
    };
};
