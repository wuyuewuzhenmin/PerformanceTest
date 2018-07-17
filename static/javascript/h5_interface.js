/**
 * Created by wuzhenmin on 2018/6/14.
 */
function Check()
{
    if ( document.getElementById("name").value=="")
    {
        alert('请输入用户名!');
        return false;
    }
     return true;
}