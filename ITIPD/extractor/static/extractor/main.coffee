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
root.coloredRanges = []

$ ->
  ($ root.typemenu).hide()
  ($ root.typemenu).menu()
  ($ root.typemenu).draggable()

  rangy.init()
  root.types = initializeCssAppliers()

  ($ root.deletebutton).click ->
    root.markedRanges.length = 0
    resetColors()

  ($ root.typemenu + " li").click color_selection

  ($('body')).mouseup (e) ->
    currentSelection = rangy.getSelection()
    showTypeMenu e.pageX, e.pageY unless isBlank currentSelection or ($ root.typemenu).is ':visible'
    ($ root.typemenu).hide() if isBlank currentSelection

  ($ root.submitbutton).click ->
    console.log root.markedRanges
    htmlString = ($ root.objecttext).clone().html()
    data = JSON.stringify root.markedRanges
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
  currentCharacterRange = rangy.getSelection().saveCharacterRanges ($ root.objecttext)[0]
  type.cssApplier.applyToSelection() for type in root.types when type.id is parseInt typeid, 10

  ($ root.typemenu).hide()

  resetColors()

  currentRange = rangy.serializeRange rangy.getSelection().getRangeAt(0), false, ($ root.objecttext)[0]
  root.markedRanges.push { type: typeid, serializedRange: currentRange, characterRange: currentCharacterRange }

  rangy.getSelection().removeAllRanges()
  redrawColors()

###
   This function draws all saved ranges in their respective colors to the objecttext.
   It also creates mouseover handlers for all those ranges.
###
redrawColors = ->
  root.markedRanges.map (elem) ->

    #recreate range with start and end from markedRanges
    range = rangy.createRange ($ root.objecttext)[0]
    range.selectCharacters ($ root.objecttext)[0], elem.characterRange[0].characterRange.start, elem.characterRange[0].characterRange.end

    #find correct color for this range in types array and mark it
    root.types.map (type) ->
      if type.id is parseInt elem.type, 10
        type.cssApplier.applyToRange range

        #get all nodes created by the cssClassApplier (the <span> elements)
        nodes = range.getNodes [1], (el) ->
          rangy.CssClassApplier.util.hasClass el, type.cssApplier.cssClass
        nodes.push range.startContainer.parentNode if nodes.length is 0
        addDeleteHandler nodes, elem.serializedRange

addDeleteHandler = (nodes, serializedRange) ->
  nodes.map (node) ->
    ($ node).on 'click', {serializedRange: serializedRange}, (event) =>
      index = i for range, i in root.markedRanges when event.data.serializedRange is range.serializedRange
      deleteMarkedRange index


deleteMarkedRange = (index = root.markedRanges.length-1) ->
  resetColors()
  root.markedRanges.splice index, 1
  redrawColors()