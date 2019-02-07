using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;

namespace JsonExample
{

    class Role
    {
        [JsonProperty("game")]
        public string Name { get; set; }
    }

    class Program
    {
        static void Main(string[] args)
        {
            string json = @"{ 'name': 'Admin', 'game': 'x' }{ 'name': 'Publisher' }";

            IList<Role> roles = new List<Role>();

            JsonTextReader reader = new JsonTextReader(new StringReader(json));
            reader.SupportMultipleContent = true;

            while (true)
            {
                if (!reader.Read())
                {
                    Console.WriteLine("Couldn't read any more...");
                    break;
                }

                Console.WriteLine("Something was read.");

                JsonSerializer serializer = new JsonSerializer();
                Role role = serializer.Deserialize<Role>(reader);

                roles.Add(role);
            }

            foreach (Role role in roles)
            {
                Console.WriteLine(role.Name);
            }

            Console.WriteLine("Hello World!");
        }
    }
}
