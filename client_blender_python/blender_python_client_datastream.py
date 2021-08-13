#import bpy
import socket
import json

'''
class TestPanel(bpy.types.Panel):
    bl_label = "Test Panel"
    bl_idname = "PT_TestPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "My 1st Addon"

    def draw (self, context):
        layout = self.layout
        row = layout.row()
        row.label(text = "Sample Text")



def register():
    bpy.utils.register_class(TestPanel)

def unregister():
    bpy.utils.unregister_class(TestPanel)
'''


def socket_client_face_landmark():
    HEADERSIZE = 10
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 5002        # The port used by the server

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((HOST, PORT))

    while True:
        full_pack = ''
        new_pack = True
        while True:
            pack = soc.recv(10)
            if new_pack:
                #print("new pack len:", pack[:HEADERSIZE])
                packlen_str = pack[:HEADERSIZE]
                packlen = int(pack[:HEADERSIZE])
                new_pack = False

            #print(f"full pack length: {packlen}")

            full_pack += pack.decode("utf-8")

            #print(len(full_pack))

            if len(full_pack) - HEADERSIZE == packlen:
                print("full package recvd")
                pack = full_pack[HEADERSIZE:]
                #print(pack)
                jpackage = json.loads(pack)
                
                # extract information
                result = "frame: " + str(jpackage['frame']) + ", fps: " + str(jpackage['fps'])
                #obj = bpy.context.object
                #obj.data.body = result
                print(result)
                
                new_pack = True
                full_pack = ""


if __name__ == "__main__":
    #bpy.ops.object.text_add()
    socket_client_face_landmark()
    
    