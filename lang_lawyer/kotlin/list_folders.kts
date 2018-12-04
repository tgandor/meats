#!/snap/bin/kotlinc -script

import java.io.File

// this illustrates the lack of ternary operator, but expression-if instead
// array length is called .size

// type can be inferred:
// val dir: String = if(args.size < 1) "." else args[0]
val dir = if(args.size < 1) "." else args[0]

val folders = File(dir).listFiles { file -> file.isDirectory() }

folders?.forEach { folder -> println(folder) }
