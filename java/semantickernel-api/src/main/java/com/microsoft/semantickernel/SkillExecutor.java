// Copyright (c) Microsoft. All rights reserved.
package com.microsoft.semantickernel;

<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
import java.util.Map;

import javax.annotation.Nullable;

<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head
import com.microsoft.semantickernel.exceptions.SkillsNotFoundException;
import com.microsoft.semantickernel.semanticfunctions.SemanticFunctionConfig;
import com.microsoft.semantickernel.skilldefinition.ReadOnlyFunctionCollection;
import com.microsoft.semantickernel.skilldefinition.ReadOnlySkillCollection;
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
import java.util.Map;
import javax.annotation.Nullable;
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< Updated upstream
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes

public interface SkillExecutor {

    /**
     * Import a set of skills
     *
     * @param skillName name of the skill
     * @param skills map of skill names to skill configs
     * @return the function collection
     * @throws SkillsNotFoundException if the skill is not found
     */
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    ReadOnlyFunctionCollection importSkill(
            String skillName, Map<String, SemanticFunctionConfig> skills)
            throws SkillsNotFoundException;
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    @Deprecated
    default ReadOnlyFunctionCollection importSkill(
            String skillName, Map<String, SemanticFunctionConfig> skills)
            throws SkillsNotFoundException { 
                throw new UnsupportedOperationException("Deprecated"); 
        }
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
    @Deprecated
    default ReadOnlyFunctionCollection importSkill(
            String skillName, Map<String, SemanticFunctionConfig> skills)
            throws SkillsNotFoundException { 
                throw new UnsupportedOperationException("Deprecated"); 
        }
<<<<<<< div
>>>>>>> main
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head

    /**
     * Get function collection with the skill name
     *
     * @param skillName name of the skill
     * @return the function collection
     * @throws SkillsNotFoundException if the skill is not found
     */
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    ReadOnlyFunctionCollection getSkill(String skillName) throws SkillsNotFoundException;
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< Updated upstream
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
    @Deprecated
    default ReadOnlyFunctionCollection getSkill(String skillName) throws SkillsNotFoundException { 
                throw new UnsupportedOperationException("Deprecated"); 
        }
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head

    /**
     * Imports the native functions annotated on the given object as a skill.
     *
     * @param skillName name of the skill
     * @return the function collection
     */
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    ReadOnlyFunctionCollection importSkillFromDirectory(
            String skillName, String parentDirectory, String skillDirectoryName);

    /** Imports the native functions annotated on the given object as a skill. */
    void importSkillsFromDirectory(String parentDirectory, String... skillNames);
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< Updated upstream
    @Deprecated
    default ReadOnlyFunctionCollection importSkillFromDirectory(
            String skillName, String parentDirectory, String skillDirectoryName) { 
                throw new UnsupportedOperationException("Deprecated"); 
        }

    /** Imports the native functions annotated on the given object as a skill. */
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
    @Deprecated
    default ReadOnlyFunctionCollection importSkillFromDirectory(
            String skillName, String parentDirectory, String skillDirectoryName) { 
                throw new UnsupportedOperationException("Deprecated"); 
        }

    /** Imports the native functions annotated on the given object as a skill. */
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
    @Deprecated
    default ReadOnlyFunctionCollection importSkillFromDirectory(
            String skillName, String parentDirectory, String skillDirectoryName) { 
                throw new UnsupportedOperationException("Deprecated"); 
        }

    /** Imports the native functions annotated on the given object as a skill. */
>>>>>>> main
=======
<<<<<<< Updated upstream
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
    @Deprecated
    default void importSkillsFromDirectory(String parentDirectory, String... skillNames) { 
                throw new UnsupportedOperationException("Deprecated"); 
        }
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head

    /**
     * Imports the native functions annotated on the given object as a skill. Assumes that the
     * directory that contains the skill is the same as skillName
     *
     * @param skillName name of the skill
     * @param parentDirectory directory that contains the skill
     * @return the function collection
     */
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    ReadOnlyFunctionCollection importSkillFromDirectory(String skillName, String parentDirectory);
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< Updated upstream
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
    @Deprecated
    default ReadOnlyFunctionCollection importSkillFromDirectory(String skillName, String parentDirectory) { 
                throw new UnsupportedOperationException("Deprecated"); 
        }
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head

    /**
     * Imports a skill using ClassLoader.getResourceAsStream to load skills from the classpath.
     *
     * @param pluginDirectory directory within the classpath that contains the skill
     * @param skillName name of the skill
     * @param functionName name of the function
     * @return the function collection
<<<<<<< AI
=======
<<<<<<< HEAD
>>>>>>> main
     * @throws KernelException if it is not possible to correctly load the skill
     */
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> origin/main
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
=======
>>>>>>> head
    ReadOnlyFunctionCollection importSkillFromResources(
            String pluginDirectory, String skillName, String functionName) throws KernelException;
<<<<<<< AI
     */
    ReadOnlyFunctionCollection importSkillFromResources(
            String pluginDirectory, String skillName, String functionName);
=======
=======
     */
    ReadOnlyFunctionCollection importSkillFromResources(
            String pluginDirectory, String skillName, String functionName);
>>>>>>> beeed7b7a795d8c989165740de6ddb21aeacbb6f
>>>>>>> main
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head
=======
>>>>>>> origin/main
=======
=======
<<<<<<< main
=======
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
=======
>>>>>>> Stashed changes
    @Deprecated
    default ReadOnlyFunctionCollection importSkillFromResources(
            String pluginDirectory, String skillName, String functionName) throws KernelException { 
                throw new UnsupportedOperationException("Deprecated"); 
        }
>>>>>>> origin/dsgrieve/java-v1-api
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head

    /**
     * Imports a skill using clazz.getResourceAsStream to load skills from the classpath.
     *
     * @param skillName name of the skill
     * @param functionName name of the function
     * @param clazz class that contains the skill
     * @return the function collection
<<<<<<< AI
=======
<<<<<<< HEAD
>>>>>>> main
     * @throws KernelException if it is not possible to correctly load the skill
     */
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
>>>>>>> head
    ReadOnlyFunctionCollection importSkillFromResources(
            String pluginDirectory, String skillName, String functionName, @Nullable Class clazz) throws KernelException;
<<<<<<< AI
     */
    ReadOnlyFunctionCollection importSkillFromResources(
            String pluginDirectory, String skillName, String functionName, @Nullable Class clazz);
=======
=======
     */
    ReadOnlyFunctionCollection importSkillFromResources(
            String pluginDirectory, String skillName, String functionName, @Nullable Class clazz);
>>>>>>> beeed7b7a795d8c989165740de6ddb21aeacbb6f
>>>>>>> main
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head
=======
>>>>>>> origin/main
=======
=======
<<<<<<< main
=======
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
=======
>>>>>>> Stashed changes
    @Deprecated
    default  ReadOnlyFunctionCollection importSkillFromResources(
            String pluginDirectory, String skillName, String functionName, @Nullable Class clazz)
            throws KernelException { 
                throw new UnsupportedOperationException("Deprecated"); 
        }
>>>>>>> origin/dsgrieve/java-v1-api
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head

    /**
     * Imports the native functions annotated on the given object as a skill.
     *
     * @param nativeSkill object containing the native functions
     * @param skillName name of the skill
     * @return the function collection
     */
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    ReadOnlyFunctionCollection importSkill(Object nativeSkill, @Nullable String skillName);
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< Updated upstream
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
    @Deprecated
    default ReadOnlyFunctionCollection importSkill(Object nativeSkill, @Nullable String skillName) { 
                throw new UnsupportedOperationException("Deprecated"); 
        }
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head

    /**
     * @return Reference to the read-only skill collection containing all the imported functions
     */
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    ReadOnlySkillCollection getSkills();
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< Updated upstream
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
    @Deprecated
    default ReadOnlySkillCollection getSkills() { 
                throw new UnsupportedOperationException("Deprecated"); 
        }
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
}
