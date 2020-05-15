import Cookie from 'js-cookie'
export default{
    getcookiesInserver: function(req){
        let servie_cookie ={};
        req && req.headers.cookie && req.headers.split(';').forEach(function(val){
        let parts = val.split('=')
        servie_cookie[parts[0].trim()] = (parts[1]|| '').trim();
        }

    }
}