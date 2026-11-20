import AppKit
import Foundation
func fail(_ text: String) -> Never { fputs(text + "\n", stderr); exit(1) }
let a = CommandLine.arguments
 guard a.count == 8 else { fail("Usage: swift normalize.swift INPUT OUTPUT TOP_Y CHIN_Y SIZE DPI HEAD_RATIO") }
guard let top=Double(a[3]), let chin=Double(a[4]), let size=Int(a[5]), let dpi=Double(a[6]), let ratio=Double(a[7]), size>0, dpi>0, ratio>0, ratio<1, top>=0, chin>top else { fail("Invalid geometry or output parameters") }
let input=URL(fileURLWithPath:a[1]).standardizedFileURL
let output=URL(fileURLWithPath:a[2]).standardizedFileURL
guard input != output else { fail("Refusing to overwrite input") }
guard !FileManager.default.fileExists(atPath:output.path) else { fail("Output exists; use a new staging path") }
guard let source=NSImage(contentsOf:input) else { fail("Cannot read input") }
var rect=CGRect(origin:.zero,size:source.size)
guard let cg=source.cgImage(forProposedRect:&rect,context:nil,hints:nil), chin<Double(cg.height) else { fail("Cannot decode image or chin lies outside image") }
let scale=Double(size)*ratio/(chin-top)
let w=Double(cg.width)*scale, h=Double(cg.height)*scale
let margin=Double(size)*0.04
// Bottom align unless that clips the crown; then preserve a 4% top margin.
let y=min(0,Double(size)-h+top*scale-margin)
guard let ctx=CGContext(data:nil,width:size,height:size,bitsPerComponent:8,bytesPerRow:0,space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue) else { fail("Cannot allocate canvas") }
ctx.interpolationQuality = .high
ctx.draw(cg,in:CGRect(x:(Double(size)-w)/2,y:y,width:w,height:h))
guard let result=ctx.makeImage() else { fail("Cannot render output") }
let rep=NSBitmapImageRep(cgImage:result)
rep.size=NSSize(width:Double(size)*72/dpi,height:Double(size)*72/dpi)
guard let data=rep.representation(using:.png,properties:[:]) else { fail("Cannot encode PNG") }
do { try FileManager.default.createDirectory(at:output.deletingLastPathComponent(),withIntermediateDirectories:true); try data.write(to:output,options:.atomic) } catch { fail(error.localizedDescription) }
let finalTop=Double(size)-(y+h)+top*scale
print("Exported. Expected crown y=\(finalTop), chin y=\(finalTop+Double(size)*ratio). Verify visually; geometry alone is not acceptance.")
