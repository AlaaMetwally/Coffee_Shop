/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-ot29rrjz', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: '5XQX3X0IbZc7ZbxqX4N4hp1Z8LYNp5Om', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8080', // the base url of the running ionic application. 
  }
};
