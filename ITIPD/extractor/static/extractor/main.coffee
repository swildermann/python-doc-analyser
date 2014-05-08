root = exports ? this

$ = jQuery
root.types = [ "markedtext",
            "functionalityandbehavior",
            "concepts",
            "directives",
            "purposes",
            "qualityattributes",
            "controlflow",
            "structure",
            "patterns",
            "codeexamples",
            "environment",
            "external",
            "noninformation" ]

root.xyz = ($ '#objecttext')

$ ->
  ($ '#deletebutton').click ->
    resetColors

resetColors = ->
  resetColor type for type in types

resetColor = (type) ->
  objecttext.find('span.#{root.types}').contents().unwrap()
