var keywords = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  // url points to a json file that contains an array of keywords
  prefetch: '/database/keywords.json'
});

// passing in `null` for the `options` arguments will result in the default
// options being used
$('#autocomplete .typeahead').typeahead(null, {
  name: 'keywords',
  source: keywords
});