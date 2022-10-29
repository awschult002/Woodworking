# ###################################################################################################################
#
# Functions to handle many toolbar icons without code duplication. Should not be used for single icon click. 
# For single icon use dedicated file to not make this library too big, and slow to load.
#
# The funtions below have error handling and pop-ups, so not call it in loop, or from other functions 
# because you get many pop-ups in case of error. No need to return anything for further processing.
#
# ###################################################################################################################


import FreeCAD, FreeCADGui
import MagicPanels

translate = FreeCAD.Qt.translate

def QT_TRANSLATE_NOOP(context, text):
	return text


# ###################################################################################################################
def panelDefault(iType):
	
	try:

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panel"+iType)

		if iType == "XY":
			panel.Length = 600
			panel.Width = 300
			panel.Height = 18

		if iType == "YX":
			panel.Length = 300
			panel.Width = 600
			panel.Height = 18

		if iType == "XZ":
			panel.Length = 600
			panel.Width = 18
			panel.Height = 300

		if iType == "ZX":
			panel.Length = 300
			panel.Width = 18
			panel.Height = 600

		if iType == "YZ":
			panel.Length = 18
			panel.Width = 600
			panel.Height = 300

		if iType == "ZY":
			panel.Length = 18
			panel.Width = 300
			panel.Height = 600

		color = (247 / 255, 185 / 255, 108 / 255, 0.0)
		panel.ViewObject.ShapeColor = color

		FreeCAD.ActiveDocument.recompute()
	
	except:
	
		info = ""
		
		info += translate('panelDefaultInfo', '<b>To create default panel, first create active document. </b><br><br><b>Note:</b> This tool creates default panel that can be easily resized. You can clearly see where should be the thickness to keep exact panel XYZ axis orientation. All furniture elements should be created according to the XYZ axis plane, if possible. Avoid building whole furniture with rotated elements. If you want to rotate panel with dowels, better create panel with dowels without rotation, pack panel with dowels into LinkGroup, and use magicAngle to rotate whole LinkGroup. You can rotate whole furniture like this with single click.')

		MagicPanels.showInfo("panelDefault"+iType, info)


# ###################################################################################################################
def panelCopy(iType):
	
	try:

		gObj = MagicPanels.getReference()
		
		[ Length, Width, Height ] = MagicPanels.sizesToCubePanel(gObj, iType)
		
		panel = FreeCAD.activeDocument().addObject("Part::Box", "panel"+iType)
		[ panel.Length, panel.Width, panel.Height ] = [ Length, Width, Height ]

		try:
			MagicPanels.copyColors(gObj, panel)
		except:
			skip = 1

		FreeCAD.ActiveDocument.recompute()

	except:

		info = ""
		
		info += translate('panelCopyInfo', '<b>To create copy of panel in exact direction, select valid panel first. </b><br><br><b>Note:</b> This tool copy selected panel into exact XYZ axis orientation. By default you can copy any panel based on Cube object. If you want to copy Pad, you need to have Constraints named "SizeX" and "SizeY" at the Sketch. For custom objects types you need to have Length, Width, Height properties at object (Group: "Base", Type: "App::PropertyLength"). The new panel will be created at (0, 0, 0) coordinate XYZ axis position. You can use mapPosition tool to move the new panel to the original panel position. To copy panel without changing orientation, you can use magicMove tool or CTRL-C and CTRL-V keys with arrows to move the copy.') 

		MagicPanels.showInfo("panelCopy"+iType, info)


# ###################################################################################################################
def panelFace(iType):
	
	try:

		gSO = FreeCADGui.Selection.getSelection()[0]
		
		gObj = MagicPanels.getReference(gSO)
		gFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		
		[ L, W, H ] = MagicPanels.sizesToCubePanel(gObj, iType)
		
		if gObj.isDerivedFrom("Part::Box"):
			[ x, y, z ] = MagicPanels.getVertex(gFace, 0, 1)
		else:
			[ x, y, z ] = MagicPanels.getVertex(gFace, 1, 0)
		
		if gSO.isDerivedFrom("Part::Cut"):
			[ x, y, z ] = MagicPanels.getVertex(gFace, 2, 0)

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelFace"+iType)
		panel.Length, panel.Width, panel.Height = L, W, H

		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
		
		try:
			MagicPanels.copyColors(gObj, panel)
		except:
			skip = 1
			
		FreeCAD.ActiveDocument.recompute()

	except:
		
		info = ""
		
		info += translate('panelFaceInfo', '<b>Please select face to create panel. </b><br><br><b>Note:</b> This tool creates new panel at selected face. The blue panel represents the selected object and the red one represents the new created object. The icon refers to base XY model view (0 key position). Click fitModel to set model into referred view. The new created panel will get the same dimensions as panel of the selected face. If you have problem with unpredicted result, use magicManager tool to preview panel before creation.')

		MagicPanels.showInfo("panelFace"+iType, info)


# ###################################################################################################################
def panelBetween(iType):
	
	try:

		gSO = FreeCADGui.Selection.getSelection()[0]
		gObj = MagicPanels.getReference(gSO)
		
		gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
	
		[ x1, y1, z1 ] = MagicPanels.getVertex(gFace1, 0, 1)
		[ x2, y2, z2 ] = MagicPanels.getVertex(gFace2, 0, 1)

		x = abs(x2 - x1)
		y = abs(y2 - y1)
		z = abs(z2 - z1)

		panel = FreeCAD.activeDocument().addObject("Part::Box", "panelBetween"+iType)
		[ panel.Length, panel.Width, panel.Height ] = MagicPanels.sizesToCubePanel(gObj, iType)

		z1 = z1 + gObj.Height.Value - panel.Height.Value
		
		if x > 0:
			panel.Length = x
		
		if y > 0:
			panel.Width = y
			
		if z > 0:
			panel.Height = z

		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z1), FreeCAD.Rotation(0, 0, 0))
		
		try:
			MagicPanels.copyColors(gObj, panel)
		except:
			skip = 1

		FreeCAD.ActiveDocument.recompute()

	except:
		
		info = ""
		
		info += translate('panelBetweenInfo', '<b>Please select two valid faces at two different valid objects, to create panel between them. </b><br><br><b>Note:</b> This tool creates new panel between two selected faces. Selection faces order is important. To select more than one face, hold left CTRL key during second face selection. The blue panels represents the selected objects and the red one represents the new created object. The icon refers to base XY model view (0 key position). Click fitModel to set model into referred view.  If the two selected panels will be matching the icon, the new created panel should fill the gap between the selected faces. You can experiment with selection faces outside to resize the new panel. If you have problem with unpredicted result, use magicManager tool to preview panel before creation.')

		MagicPanels.showInfo("panelBetween"+iType, info)


# ###################################################################################################################
def panelSide(iType):
	
	try:

		gObj = MagicPanels.getReference()
		gFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]

		[ Length, Width, Height ] = MagicPanels.sizesToCubePanel(gObj, "ZY")

		if gObj.isDerivedFrom("Part::Box"):
			[ x, y, z ] = MagicPanels.getVertex(gFace, 0, 1)

		else:

			if iType == "1" or iType == "2":
				[ x, y, z ] = MagicPanels.getVertex(gFace, 0, 0)

			if iType == "3" or iType == "4":
				[ x, y, z ] = MagicPanels.getVertex(gFace, 1, 0)

		if iType == "1":
			x = x - Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideLeft")
		
		if iType == "2":
			z = z + Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideLeftUP")
		
		if iType == "3":
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideRight")
		
		if iType == "4":
			x = x - Length
			z = z + Length
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelSideRightUP")

		panel.Length = Length
		panel.Width = Width
		panel.Height = Height
		
		panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(0, 0, 0))
		
		try:
			MagicPanels.copyColors(gObj, panel)
		except:
			skip = 1

		FreeCAD.ActiveDocument.recompute()

	except:
		
		info = ""
		
		info += translate('panelSideInfo', '<b>Please select valid face, to create panel. </b><br><br><b>Note:</b> This tool creates new panel at selected face. The blue panel represents the selected object and the red one represents the new created object. The arrow describe if the panel will be created up or down. The icon refers to base XY model view (0 key position). Click fitModel to set model into referred view. If you have problem with unpredicted result, use magicManager tool to preview panel before creation.')

		if iType == "1":
			MagicPanels.showInfo("panelSideLeft", info)
		if iType == "2":
			MagicPanels.showInfo("panelSideLeftUP", info)
		if iType == "3":
			MagicPanels.showInfo("panelSideRight", info)
		if iType == "4":
			MagicPanels.showInfo("panelSideRightUP", info)


# ###################################################################################################################
def panelBackOut():
	
	try:

		gObj = MagicPanels.getReference()

		gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
		gFace3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]

		[ x, y, z ] = MagicPanels.sizesToCubePanel(gObj, "ZX")

		[ x1, y1, z1 ] = MagicPanels.getVertex(gFace1, 0, 1)
		[ x2, y2, z2 ] = MagicPanels.getVertex(gFace2, 0, 0)
		[ x3, y3, z3 ] = MagicPanels.getVertex(gFace3, 0, 1)

		x = abs(x2 - x1)
		z = z - z3

		if x > 0 and y > 0 and z > 0:

			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelBackOut")
			panel.Length = x
			panel.Width = y
			panel.Height = z

			panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z3), FreeCAD.Rotation(0, 0, 0))
			
			try:
				MagicPanels.copyColors(gObj, panel)
			except:
				skip = 1

			FreeCAD.ActiveDocument.recompute()
			
		else:
		
			raise

	except:
			
		info = ""
		
		info += translate('panelBackOutInfo', '<b>Please select three faces according to the icon. </b><br><br><b>Note:</b> This tool allows to create back of the furniture with single click. To create back of the furniture you have to select 3 faces in the order described by the icon. To select more than one face, hold left CTRL key during face selection. The red edges at blue panels represents the selected faces. The transparent red panel represents the new created object. The icon refers to the back of the furniture.')
		
		MagicPanels.showInfo("panelBackOut", info)


# ###################################################################################################################
def panelCover(iType):
	
	try:

		gObj = MagicPanels.getReference()
		
		gFace1 = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]
		gFace2 = FreeCADGui.Selection.getSelectionEx()[1].SubObjects[0]
		gFace3 = FreeCADGui.Selection.getSelectionEx()[2].SubObjects[0]

		[ x, y, z ] = MagicPanels.sizesToCubePanel(gObj, iType)

		[ x1, y1, z1 ] = MagicPanels.getVertex(gFace1, 0, 1)
		[ x2, y2, z2 ] = MagicPanels.getVertex(gFace2, 2, 1)
		[ x3, y3, z3 ] = MagicPanels.getVertex(gFace3, 0, 1)

		x = abs(x2 - x1)
		y = y + z

		if x > 0 and y > 0 and z > 0:
		
			panel = FreeCAD.activeDocument().addObject("Part::Box", "panelCover"+iType)
			panel.Length = x
			panel.Width = y
			panel.Height = z

			panel.Placement = FreeCAD.Placement(FreeCAD.Vector(x1, y1, z3), FreeCAD.Rotation(0, 0, 0))
			
			try:
				MagicPanels.copyColors(gObj, panel)
			except:
				skip = 1

			FreeCAD.ActiveDocument.recompute()

	except:
		
		info = ""
		
		info += translate('panelCoverInfo', '<b>Please select three faces according to the icon. </b><br><br><b>Note:</b> This tool allows to create top cover of the furniture with single click. To create top cover of the furniture you have to select 3 faces in the order described by the icon. To select more than one face, hold left CTRL key during face selection. The red edges at blue panels represents the selected faces. The transparent red panel represents the new created object. The icon refers to the base XY model view (0 key position). Click fitModel to set model into referred view.')

		MagicPanels.showInfo("panelCover"+iType, info)


# ###################################################################################################################
def panelMove(iType):
	
	try:

		selection = FreeCADGui.Selection.getSelection()
		
		for o in selection:

			gObj = MagicPanels.getReference(o)

			sizes = []
			sizes = MagicPanels.getSizes(gObj)
			sizes.sort()

			x = 0
			y = 0
			z = 0
			
			if iType == "Xp":
				x = sizes[0]
			
			if iType == "Xm":
				x = - sizes[0]

			if iType == "Yp":
				y = sizes[0]

			if iType == "Ym":
				y = - sizes[0]

			if iType == "Zp":
				z = sizes[0]

			if iType == "Zm":
				z = - sizes[0]

			try:
				[ x, y, z ] = MagicPanels.convertPosition(gObj, x, y, z)
			except:
				skip = 1
				
			[ x, y, z ] = MagicPanels.getModelRotation(x, y, z)

			[ px, py, pz, r ] = MagicPanels.getPlacement(gObj)
			MagicPanels.setPlacement(gObj, px+x, py+y, pz+z, r)

			FreeCAD.ActiveDocument.recompute()
	
	except:
		
		info = ""
		
		info += translate('panelMoveInfo', '<b>Please select valid objects to move. </b><br><br><b>Note:</b> With the arrows you can quickly move many Cube panels or even any other objects at once. If the thickness of the selected object can be recognized, the move step will be the thickness. So, you can solve common furniture problem with thickness offset. If the thickness will not be recognized the step will be 100. This allow you to move whole furniture segments very quickly. The arrows recognize the view model rotation. If you want precisely move object, use magicMove tool, instead. ')
		
		MagicPanels.showInfo("panelMove"+iType, info)


# ###################################################################################################################
def panelResize(iType):
	
	try:

		objects = FreeCADGui.Selection.getSelection()
		
		if len(objects) < 1:
			raise
		
		for o in objects:

			gObj = MagicPanels.getReference(o)

			sizes = []
			sizes = MagicPanels.getSizes(gObj)
			sizes.sort()
			thick = sizes[0]

			if gObj.isDerivedFrom("Part::Cylinder"):
				
				R, H = gObj.Radius.Value, gObj.Height.Value
				
				if iType == "1":
					gObj.Height = gObj.Height.Value + thick

				if iType == "2":
					if H - thick > 0:
						gObj.Height = gObj.Height.Value - thick

				if iType == "3":
					gObj.Radius = gObj.Radius.Value + thick
					
				if iType == "4":
					if R - thick > 0:
						gObj.Radius = gObj.Radius.Value - thick

				if iType == "5":
					gObj.Radius = gObj.Radius.Value + thick/2

				if iType == "6":
					if R - thick/2 > 0:
						gObj.Radius = gObj.Radius.Value - thick/2

			if gObj.isDerivedFrom("Part::Cone"):
				
				R1, R2, H = gObj.Radius1.Value, gObj.Radius2.Value, gObj.Height.Value
				
				if iType == "1":
					gObj.Height = gObj.Height.Value + thick

				if iType == "2":
					if H - thick > 0:
						gObj.Height = gObj.Height.Value - thick

				if iType == "3":
					gObj.Radius2 = gObj.Radius2.Value + thick/2

				if iType == "4":
					if R2 - thick/2 > 0:
						gObj.Radius2 = gObj.Radius2.Value - thick/2

				if iType == "5":
					gObj.Radius1 = gObj.Radius1.Value + thick/2

				if iType == "6":
					if R1 - thick/2 > 0:
						gObj.Radius1 = gObj.Radius1.Value - thick/2

			if gObj.isDerivedFrom("Part::Box"):

				L, W, H = gObj.Length.Value, gObj.Width.Value, gObj.Height.Value
					
				if iType == "1":
					if L == sizes[2]:
						gObj.Length = gObj.Length.Value + thick

					if W == sizes[2]:
						gObj.Width = gObj.Width.Value + thick
						
					if H == sizes[2]:
						gObj.Height = gObj.Height.Value + thick

				if iType == "2":
					if L == sizes[2]:
						if gObj.Length.Value - thick > 0:
							gObj.Length = gObj.Length.Value - thick
						
					if W == sizes[2]:
						if gObj.Width.Value - thick > 0:
							gObj.Width = gObj.Width.Value - thick
						
					if H == sizes[2]:
						if gObj.Height.Value - thick > 0:
							gObj.Height = gObj.Height.Value - thick

				if iType == "3":
					if L == sizes[1]:
						gObj.Length = gObj.Length.Value + thick

					if W == sizes[1]:
						gObj.Width = gObj.Width.Value + thick

					if H == sizes[1]:
						gObj.Height = gObj.Height.Value + thick

				if iType == "4":
					if L == sizes[1]:
						if gObj.Length.Value - thick > 0:
							gObj.Length = gObj.Length.Value - thick

					if W == sizes[1]:
						if gObj.Width.Value - thick > 0:
							gObj.Width = gObj.Width.Value - thick

					if H == sizes[1]:
						if gObj.Height.Value - thick > 0:
							gObj.Height = gObj.Height.Value - thick

				if iType == "5":
					if L == sizes[0]:
						gObj.Length = gObj.Length.Value + 1

					if W == sizes[0]:
						gObj.Width = gObj.Width.Value + 1

					if H == sizes[0]:
						gObj.Height = gObj.Height.Value + 1

				if iType == "6":
					if L == sizes[0]:
						if gObj.Length.Value - 1 > 0:
							gObj.Length = gObj.Length.Value - 1

					if W == sizes[0]:
						if gObj.Width.Value - 1 > 0:
							gObj.Width = gObj.Width.Value - 1

					if H == sizes[0]:
						if gObj.Height.Value - 1 > 0:
							gObj.Height = gObj.Height.Value - 1

			if gObj.isDerivedFrom("PartDesign::Pad"):
			
				[ sizeX, sizeY, thick ] = MagicPanels.getSizes(gObj)
				
				if iType == "1":
					
					if sizeX > sizeY:
						gObj.Profile[0].setDatum("SizeX", FreeCAD.Units.Quantity(sizeX + thick))
					else:
						gObj.Profile[0].setDatum("SizeY", FreeCAD.Units.Quantity(sizeY + thick))
			
				if iType == "2":
					
					if sizeX > sizeY:
						if sizeX - thick > 0:
							gObj.Profile[0].setDatum("SizeX", FreeCAD.Units.Quantity(sizeX - thick))
					else:
						if sizeY - thick > 0:
							gObj.Profile[0].setDatum("SizeY", FreeCAD.Units.Quantity(sizeY - thick))

				if iType == "3":
					
					if sizeX < sizeY:
						gObj.Profile[0].setDatum("SizeX", FreeCAD.Units.Quantity(sizeX + thick))
					else:
						gObj.Profile[0].setDatum("SizeY", FreeCAD.Units.Quantity(sizeY + thick))
			
				if iType == "4":
					
					if sizeX < sizeY:
						if sizeX - thick > 0:
							gObj.Profile[0].setDatum("SizeX", FreeCAD.Units.Quantity(sizeX - thick))
					else:
						if sizeY - thick > 0:
							gObj.Profile[0].setDatum("SizeY", FreeCAD.Units.Quantity(sizeY - thick))
				
				if iType == "5":
					
					if o.isDerivedFrom("PartDesign::Thickness"):
						o.Value.Value = o.Value.Value + 1
					else:
						gObj.Length = gObj.Length.Value + 1
				
				if iType == "6":
					
					if o.isDerivedFrom("PartDesign::Thickness"):
						if o.Value.Value -1 > 0:
							o.Value.Value = o.Value.Value - 1
					else:
						if gObj.Length.Value - 1 > 0:
							gObj.Length = gObj.Length.Value - 1
					

		FreeCAD.ActiveDocument.recompute()
	
	except:
		
		info = ""
		
		info += translate('panelResizeInfo', '<b>Please select valid panels to resize. </b><br><br><b>Note:</b> This tool allows to resize quickly panels or even other objects. The resize step is the panel thickness. Panel is resized into direction described by the icon for XY panel. However, in some cases the panel may be resized into opposite direction, if the panel is not supported or the sides are equal. You can also resize Cylinders (drill bits), the long side will be Height, the short will be diameter, the thickness will be Radius. For Cone objects (drill bits - countersinks, counterbore) the long side will be Height, the thickness will be Radius1 (bottom radius) and the short will be Radius2 (top radius).')
		
		MagicPanels.showInfo("panelResize"+iType, info)


# ###################################################################################################################
