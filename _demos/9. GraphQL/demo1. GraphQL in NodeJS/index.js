let { graphql, buildSchema } = require('graphql');

var schema = buildSchema (`
    type Query { 
        hello: String,
    }
`);

var root = { hello: () => `hello world ${Date.now()}`};

graphql(schema, '{ hello }', root).then((response) => {
    console.log(response);
});