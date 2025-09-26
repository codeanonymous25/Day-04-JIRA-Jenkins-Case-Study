node {

stage("Build"){
checkout scm
}

stage("Testing"){

try{
sh'''
python3 test.py
'''

}catch(err){
currentBuild.result="FAILURE"

}



}
if (env.CHANGE_ID && (currentBuild.result==null || currentBuild.result=="SUCCESS")){
stage("Yoo"){

input message: "test passes lets merge", ok: "Approve"
}

} 

}
