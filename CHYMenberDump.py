#!/usr/bin/python
import string
import lldb
import fblldbbase as fb
import fblldbobjcruntimehelpers as runtimeHelpers

def lldbcommands():
    return [ PrintInstanceDump() ]

class PrintInstanceDump(fb.FBCommand):
    def name(self):
        return 'pdump'
        
    def description(self):
        return 'Print instance properties'
    
    def run(self, arguments, options):
        cls = arguments[0]
        ilass = arguments[0]
        if not self.isClassObject(cls):
            cls = runtimeHelpers.object_getClass(cls)
            if not self.isClassObject(cls):
                raise Exception('Invalid argument. Please specify an instance or a Class.')
    
        menber_json = self.get_oc_menbers_json(cls,ilass)
        print menber_json
        
    def get_oc_menbers_json(mSelf,klass,ilass):
        str = """
            unsigned int menberCount;
            NSMutableDictionary *result = (id)[NSMutableDictionary dictionary];
            objc_property_t *properties = (objc_property_t *)class_copyPropertyList((Class)$cls, &menberCount);
            for (int i = 0; i<menberCount; i++)
            {
                char *name = (char *)property_getName(properties[i]);
                NSString *ret_name = (NSString *)[NSString stringWithUTF8String:name];
                id value = (id)[(NSObject *)$ils valueForKey:ret_name]?:@"nil";
                [result setObject:value forKey:ret_name];
            }
            //free(properties);
            RETURN(result);
        """
        
        command = string.Template(str).substitute(cls=klass,ils=ilass)
        return fb.evaluate(command)
    
    def isClassObject(mSelf,arg):
            return runtimeHelpers.class_isMetaClass(runtimeHelpers.object_getClass(arg))