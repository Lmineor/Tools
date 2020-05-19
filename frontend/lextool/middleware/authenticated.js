import getCookie from '@/config/get-cookie'

export default function ({store, route, redirect, req}) {
  // If the user is not authenticated
  const {auth} = getCookie(req)
  console.log('middle')
  console.log(auth)
  if (auth) {
    store.commit('SET_AUTH', auth)
    // return store.dispatch('getUserInfo')
    return redirect('/')
  }
  const routePath = route.path
  const extraPath = ['/']
  if ((!store.state.token) && extraPath.indexOf(routePath) === -1) {
    return redirect('/login')
  }
}