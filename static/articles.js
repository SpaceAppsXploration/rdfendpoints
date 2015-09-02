function parse_concepts(response) {
  var result = [];
  for (index in response) {
    if (response[index].group == "keywords") {
      result.push(response[index].label);
    };
  };
  return result;
}

var keywords = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  // url points to a json file that contains an array of keywords
  prefetch: {
    url: 'http://chronosapi-chronoslod.rhcloud.com/concepts/c',
    transform: parse_concepts
  }
});

// passing in `null` for the `options` arguments will result in the default
// options being used
$('#autocomplete .typeahead').typeahead(null, {
  name: 'keywords',
  source: keywords
});