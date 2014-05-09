root = exports ? this

$ = jQuery
root.types = [ { name: "markedtext", id: 13, cssApplier: null }
               { name: "functionalityandbehavior", id: 1, cssApplier: null }
               { name: "concepts", id: 2, cssApplier: null }
               { name: "directives", id: 3, cssApplier: null }
               { name: "purposes", id: 4, cssApplier: null }
               { name: "qualityattributes", id: 5, cssApplier: null }
               { name: "controlflow", id: 6, cssApplier: null }
               { name: "structure", id: 7, cssApplier: null }
               { name: "patterns", id: 8, cssApplier: null }
               { name: "codeexamples", id: 9, cssApplier: null }
               { name: "environment", id: 10, cssApplier: null }
               { name: "external", id: 11, cssApplier: null }
               { name: "noninformation", id: 12, cssApplier: null } ]

root.deletebutton = '#deletebutton'
root.submitbutton = '#submitbutton'
root.typemenu = '#typemenu'
root.objecttext = '#objecttext'
root.markedRanges = []

$ ->
  ($ root.typemenu).hide()
  ($ root.typemenu).menu()
  ($ root.typemenu).draggable()

  rangy.init()
  root.types = initializeCssAppliers()

  ($ root.deletebutton).click ->
    resetColors()

  ($ root.typemenu + " li").click color_selection

  ($('body')).mouseup (e) ->
    currentSelection = rangy.getSelection()
    showTypeMenu e.pageX, e.pageY unless isBlank currentSelection or ($ root.typemenu).is ':visible'
    ($ root.typemenu).hide() if isBlank currentSelection

  ($ root.submitbutton).click ->
    htmlString = ($ root.objecttext).clone().html()
    data = JSON.stringify markedRanges
    $.post '/extractor/vote/',
      range: data
      html_text: htmlString
      unit: ($ "#documentationunitid").attr "class"
      (data) ->
        console.log "ajax request successful"
        window.location = '/extractor/myunits'

initializeCssAppliers = ->
  root.types.map (type) ->
    {
      name: type.name,
      id: type.id,
      cssApplier: rangy.createCssClassApplier type.name, {normalize: true}
    }

isEmpty = (str) ->
    not str || str.length is 0

isBlank = (str) ->
    not str || /^\s*$/.test(str)

resetColors = ->
  resetColor type for type in root.types

resetColor = (type) ->
  ($ root.objecttext).find("span.#{type.name}").contents().unwrap()

showTypeMenu = (atPositionX, atPositionY) ->
  ($ root.typemenu).css 'left', atPositionX
  ($ root.typemenu).css 'top', atPositionY
  ($ root.typemenu).show()

color_selection = (event) ->
  try
    rangy.serializeRange rangy.getSelection().getRangeAt(0), false, ($ root.objecttext)[0]
  catch err
    return

  typeid = $(@).attr "id"
  type.cssApplier.applyToSelection() for type in root.types when type.id is parseInt typeid, 10

  ($ root.typemenu).hide()

  html = ($ root.objecttext).clone()
  resetColors

  currentRange = rangy.serializeRange rangy.getSelection().getRangeAt(0), false, ($ root.objecttext)[0]
  root.markedRanges.push { type: typeid, serializedRange: currentRange }

  ($ root.objecttext).replaceWith html

  rangy.getSelection().removeAllRanges()